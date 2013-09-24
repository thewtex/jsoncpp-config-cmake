# For build tree configuration.
get_target_property( jsoncpp_LIBRARY jsoncpp_lib LOCATION )
set( jsoncpp_INCLUDE ${jsoncpp_SOURCE_DIR}/include )
configure_file( "${jsoncpp_SOURCE_DIR}/cmake/jsoncpp-config.cmake.in"
  "${jsoncpp_BINARY_DIR}/jsoncpp-config.cmake"
  )

# For install configuration.
get_filename_component( jsoncpp_INSTALL_LIBRARY
  ${jsoncpp_LIBRARY} NAME
  )
set( jsoncpp_LIBRARY ${CMAKE_INSTALL_PREFIX}/lib/${jsoncpp_INSTALL_LIBRARY} )
set( jsoncpp_INCLUDE ${CMAKE_INSTALL_PREFIX}/include )
configure_file( "${jsoncpp_SOURCE_DIR}/cmake/jsoncpp-config.cmake.in"
  "${jsoncpp_BINARY_DIR}/InstallFiles/jsoncpp-config.cmake"
  )
install(FILES
  "${jsoncpp_BINARY_DIR}/InstallFiles/jsoncpp-config.cmake"
  DESTINATION lib/cmake/jsoncpp
  COMPONENT Development
  )
