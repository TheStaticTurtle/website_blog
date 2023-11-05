
---
slug: embedding-lua-to-make-projects-modular
title: "Embedding LUA to make projects modular"
draft: false
featured: false
date: 2023-11-04T12:00:00.000Z
image: "images/cover.jpg"
tags:
  - experiments
  - Tutorials
  - c++
  - lua
authors:
  - samuel
---

Embedding LUA and some libraries into a C++ project in order to make it modular

<!--more-->

What prompted this side-project is a disccusion I had at work where we mentioned that it would be a nice idea to have a piece software that could help automatically diagnose different issues that could easily happen.


I've always wanted to find a way to easyilly make a standalone executable be able to load different source modules and execute them.

Here there are a few options that are commonly used:
  - Python
  - JS
  - Lua

I din't look very far at the other options but from what I saw, python is pretty easy to embbed and js seems to be a bit annoying.
I wanted to embed LUA beacuse the core itself is pretty light and I thought that it would be nice to know how to implement it if I wanted to do something similar on microcontrollers

## Getting started

As I didn't want to compile everything from The first thing to do was to download a precompiled version of lua (with the headers). Thankfully, on windows you can easilly download it courtesy of [luabinaries](https://sourceforge.net/projects/luabinaries). 
I specifically downloaded `lua-5.4.2_Win64_dll17_lib.zip` and extracted it somewhere in my disk.

Next the only thing to do to finish the installation was to add an environment variable name `Lua_DIR` poiting where the zip was exctrated

## Preparing the project

With the help of my IDE (CLion) I started by creating a simple c++ executable. Basically this creates basic `main.cpp` and `CMakesLists.txt` files.

Throught this project you might see mentions of [`spdlog`](https://github.com/gabime/spdlog) which is a very simple logging library. This is not important for this project nor is related to Lua.

Including Lua in a CMake project is super easy. CMakes already has a builtin `FindLua` function that will check many places, including the `Lua_DIR` environment variable. So to include lua in the project you simply have to add theses lines: 
```cmake
find_package(Lua REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE ${LUA_LIBRARIES})
target_include_directories(${PROJECT_NAME} PRIVATE  ${LUA_INCLUDE_DIR} src/)
```

And if the lua54 library isn't in the path, these lines in order to copy the dll automatically:
```cmake
if (WIN32)
    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy "$ENV{Lua_DIR}/lua${LUA_VERSION_MAJOR}${LUA_VERSION_MINOR}.dll" "$<TARGET_FILE_DIR:${PROJECT_NAME}>")
endif ()
```

As Lua is a C library and we are building a C++ project, when we include the headers we need to manually specify that what we include are C files with an `extern "C"` directive, just like this:
```c++
extern "C" {
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"
}
```
## First steps

To use Lua, the first thing to do is to create a new state. Then because lua is pretty much useless without the default libs you need to run the `luaL_openlibs(L)` function in order to initialize everything. The default startup code looks like this:
```c++
lua_State* L = luaL_newstate();
luaL_openlibs(L);

...

lua_close(L);
```

## Writting the actual app
The main goal of this project to make a program that will execute all lua files in a directory query gobal varaibles that gives out infos about the file, run a function and get the result.

Lets write a LUA module to check internet connectivity that we'll save to the `modules/network-connectivity-check.lua` file:
```lua
MODULE_ID = "network-connectivity-check"
MODULE_NAME = "Network connectivity check"
MODULE_VERSION = "1.0.0"

function main()
    local handler = io.popen("ping 1.1.1.1 -n 1")
    local response = handler:read("*a")
    return string.find(response, "Lost = 0", 1, true) ~= nil
end
```

### Loading the file

Lua has a handy dandy method to load files called `luaL_dofile` which will return if the file executed properly or not.
 - If it has, it will return `LUA_OK` and whatever is returned by the file is put on the stack.
 - If it didn't it will put the error message on the stack

The code looks like this:
```c++
if (luaL_dofile(L, "modules/network-connectivity-check.lua") != LUA_OK) {
    logger->error("Error loading file: {}", lua_tostring(L, -1));
    return -1;
}
```

As the modules are not supposed to return anything and I want to make sure that my stack is clean, I also added the line:
```c++
lua_pop(L, lua_gettop(L));
```
Which will pop the number of items in the stack essensially clearing it.

### Reading globals

The lua script I wrote exposes a few global variables that gives out infos about the script. To read globals we can use the `lua_getglobal` function which will put the content onto the stack.

To read a string the code looks like this: 
```c++
lua_getglobal(L, "MODULE_ID"); // Put the global variable MODULE_ID ontot the stack
std::string MODULE_ID = lua_tostring(L, -1); // As we know it is a string, read it directly and store it
lua_pop(L, 1); // Remove it from the stack
```

Whichs gives something like this to read everything:

```c++
// Get the global variables
lua_getglobal(L, "MODULE_ID");
std::string MODULE_ID = lua_tostring(L, -1); lua_pop(L, 1);
lua_getglobal(L, "MODULE_NAME");
std::string MODULE_NAME = lua_tostring(L, -1); lua_pop(L, 1);
lua_getglobal(L, "MODULE_VERSION");
std::string MODULE_VERSION = lua_tostring(L, -1); lua_pop(L, 1);

// Output it
logger->info("Module {}({}) version {} loaded", MODULE_ID, MODULE_NAME, MODULE_VERSION);
```

Which gives a nice message in the logs:
```
[2023-11-05 01:11:03.146] [main] [info] Module network-connectivity-check(Network connectivity check) version 1.0.0 loaded
```

### Running the test function

Now that we know about the file let's run the `main` function. The function takes in 0 arguments and is supposed to return one boolean.

So lets get the global named main and put it onto the stack:
```c++
lua_getglobal(L, "main");
```

Then we can use the `lua_pcall` function to call it and get the result. The `lua_pcall` fonction take 3 arguments, the number argument of the function taht is on the stack,  the number of things returned 
```c++
if (lua_pcall(L, 0, 1, 0) != LUA_OK) {
    logger->error("Error running function 'main': {}\n", lua_tostring(L, -1));
    return -1;
}
```
Then, we can check that the last value on the stack (the one returned by the function) is actually a boolean
```c++
if (!lua_isboolean(L, -1)) {
    logger->error("Error function 'main' must return a boolean\n");
    return -1;
}
```

And finnaly we can read it and remove it from the stack:
```c++
bool ret_value = lua_toboolean(L, -1);
lua_pop(L, 1);

logger->info("Module {} returned: {}", MODULE_ID, ret_value);
```

Which (assuming that you can reach 1.1.1.1) will print out: 
```
[2023-11-05 01:55:43.921] [main] [info] Module network-connectivity-check returned: true
```

## Libraries

Lets say that we want to do a check for DNS. We can do that easilly with the help of the `luasocket` module and this script:

```lua
function main()
    socket = require("socket")
    addr, err = socket.dns.getaddrinfo("one.one.one.one")
    return err == nil
end
```

The thing is that, as we are embedding lua, we can't simply download the DLL and helper files. Lets compile it by hand.

First I created a new `lib/luasocket` folder in my project dir. Then I got the `src` dir from the github repo:
{{< og "https://github.com/lunarmodules/luasocket/" >}}

Making it compatible with CMake is a bit more involved. First I created a `CMakeLists.txt` file in `lib/luasocket` containing:

{{< og "https://gist.github.com/TheStaticTurtle/b0f8da68128066dc45231cd87d50b1ce" >}}

Then we can add the following in the project's `CMakeLists.txt`:
```cmake
add_subdirectory("${PROJECT_SOURCE_DIR}/lib/luasocket")
target_link_libraries(${PROJECT_NAME} PRIVATE LuaSocket)
```

Finnaly we need to tell lua to actually load the library. To do that we are gonig to rewrite the `luaL_openlibs` ourselves so that we can control what get's loaded.

If we look in the [linit.c](https://github.com/lua/lua/blob/master/linit.c) file, we can see how it works so let's rewrite a function that does the same thing + import luasockets:

```c++
void luaL_custom_openlibs(lua_State* L) {
    static const luaL_Reg loadedLibs[] = {
            {LUA_GNAME, luaopen_base},
            {LUA_LOADLIBNAME, luaopen_package},
            {LUA_COLIBNAME, luaopen_coroutine},
            {LUA_TABLIBNAME, luaopen_table},
            {LUA_IOLIBNAME, luaopen_io},
            {LUA_OSLIBNAME, luaopen_os},
            {LUA_STRLIBNAME, luaopen_string},
            {LUA_MATHLIBNAME, luaopen_math},
            {LUA_UTF8LIBNAME, luaopen_utf8},
            {LUA_DBLIBNAME, luaopen_debug},
            {"socket.core", luaopen_socket_core},
            {"mime.core", luaopen_mime_core},
            {NULL, NULL}
    };

    for (const luaL_Reg* lib = loadedLibs; lib->func; lib++) {
        luaL_requiref(L, lib->name, lib->func, 1);
        lua_pop(L, 1);
    }
}
```

We also need to include the correct C headers :
```c++
extern "C" {
#include "luasocket.h"
#include "mime.h"
}
```

In the lua script if we add a: `print(require("socket.core")._VERSION)` you should see the version of LuaSocket printed out in the terminal.

Notice that it produces a error about not finding the `socket` module. That's because LuaSocket is actually a mix of .c files an .lua files.
Typically Lua will automatically look in a few places for the files. However I want to have the library fully contained in the .exe.

To do this, I choose to convert the .lua to .c/.h with the help of bin2c and include them in the build. That's not enough, we need to create our own loader function for lua's `require` function.

To do that we need to get the `LUA_LOADLIBNAME` global, then get the `searchers` field and then push a function into the list:
```c++
void luaL_custom_openpackages(lua_State* L) {
    // Get the "package" global
    lua_getglobal(L, LUA_LOADLIBNAME);
    if (!lua_istable(L, -1)) {
        logger->error("Failed to get global '" LUA_LOADLIBNAME "', value is not a table");
        return;
    }
    // Get the "package.searchers" field
    lua_getfield(L, -1, "searchers");
    if (!lua_istable(L, -1)) {
        logger->error("Failed to get global 'searchers', value is not a table");
        return;
    }
    // Add the function at the end of the table
    lua_pushvalue(L, -2);
    lua_pushcclosure(L, luaL_custom_package_loader, 1);
    lua_rawseti(L, -2, 5);
    lua_setfield(L, -2, "searchers");
}
```

Then, we can write the actual loader.  First we define a list of name / data, then we loop over everything and if we have something which name's matches, we can load the string:

```c++
int luaL_custom_package_loader(lua_State *L) {
    typedef struct luaL_LFile {
        const char *name;
        char* data;
    } luaL_LFile;

    static const luaL_LFile loadedFiles[] = {
            {"socket", (char*)luasocket_socket_lua_data},
            {"ltn12", (char*)luasocket_ltn12_lua_data},
            {"mime", (char*)luasocket_mime_lua_data},

            {"socket.http", (char*)luasocket_http_lua_data},
            {"socket.tp", (char*)luasocket_tp_lua_data},
            {"socket.ftp", (char*)luasocket_ftp_lua_data},
            {"socket.smtp", (char*)luasocket_smtp_lua_data},
            {"socket.url", (char*)luasocket_url_lua_data},
            {"socket.mbox", (char*)luasocket_mbox_lua_data},
            {"socket.headers", (char*)luasocket_headers_lua_data},

            {NULL, NULL}
    };


    //Get the name of the module to search
    const char *name = luaL_checkstring(L, 1);
    // Iterate over the lua files available locally
    const luaL_LFile *file;
    for (file = loadedFiles; file->data; file++) {
        // If we have said module locally
        if(strcmp(file->name, name) == 0) {
            // Load the lua code into the stack as the 1st argument
            if (luaL_loadstring(L, file->data) == LUA_OK) {
                // Load the name of the module into the stack as the 2nd argument
                lua_pushstring(L, file->name);
                return 2;
            } else {
                // If the code failed to load, return an error
                return luaL_error(L, "error loading integrated module '%s':\n\t%s", name, lua_tostring(L, -1));
            }
        }
    }
    // Nothing found
    return 1;
}
```

And finally we can call the function we just created at setup:
```c++
lua_State* L = luaL_newstate();
luaL_custom_openlibs(L);
luaL_custom_openpackages(L);
```

And it works:
```
[2023-11-05 03:24:31.396] [main] [info] Module network-dns-check returned: true
```

## Conclusion

Obviously this is a very basic example and I have still a lot to learn about the inner workings of Lua but it's been a nice experiment to actually embbed it into a project.