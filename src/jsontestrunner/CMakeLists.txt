find_package(PythonInterp 2.6 REQUIRED)

if(JSONCPP_LIB_BUILD_SHARED)
    add_definitions( -DJSON_DLL )
endif(JSONCPP_LIB_BUILD_SHARED)

add_executable(jsontestrunner_exe
               main.cpp
               )
target_link_libraries(jsontestrunner_exe jsoncpp_lib)
set_target_properties(jsontestrunner_exe PROPERTIES OUTPUT_NAME jsontestrunner_exe)

if(PYTHONINTERP_FOUND)
    # Run end to end parser/writer tests
    get_property(JSONTESTRUNNER_EXE_PATH TARGET jsontestrunner_exe PROPERTY LOCATION)
    set(TEST_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../../test)
    set(RUNJSONTESTS_PATH ${TEST_DIR}/runjsontests.py)
    add_custom_target(jsoncpp_readerwriter_tests ALL
                      "${PYTHON_EXECUTABLE}" -B "${RUNJSONTESTS_PATH}" "${JSONTESTRUNNER_EXE_PATH}" "${TEST_DIR}/data"
                      DEPENDS jsontestrunner_exe jsoncpp_test
                      )
    add_custom_target(jsoncpp_check DEPENDS jsoncpp_readerwriter_tests)
endif(PYTHONINTERP_FOUND)
