if(JSONCPP_LIB_BUILD_SHARED)
    add_definitions( -DJSON_DLL )
endif(JSONCPP_LIB_BUILD_SHARED)

add_executable( jsoncpp_test
                jsontest.cpp
                jsontest.h
                main.cpp
                )

target_link_libraries(jsoncpp_test jsoncpp_lib)

# Run unit tests in post-build
# (default cmake workflow hides away the test result into a file, resulting in poor dev workflow?!?)
if(JSONCPP_WITH_POST_BUILD_UNITTEST)
    add_custom_command( TARGET jsoncpp_test
                        POST_BUILD
                        COMMAND jsoncpp_test)
endif(JSONCPP_WITH_POST_BUILD_UNITTEST)

set_target_properties(jsoncpp_test PROPERTIES OUTPUT_NAME jsoncpp_test)
