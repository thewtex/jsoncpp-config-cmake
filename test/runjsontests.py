import sys
import os
import os.path
from glob import glob

RUN_JSONCHECKER = True

def compareOutputs( expected, actual, message ):
    expected = expected.strip().replace('\r','').split('\n')
    actual = actual.strip().replace('\r','').split('\n')
    diff_line = 0
    max_line_to_compare = min( len(expected), len(actual) )
    for index in xrange(0,max_line_to_compare):
        if expected[index].strip() != actual[index].strip():
            diff_line = index + 1
            break
    if diff_line == 0 and len(expected) != len(actual):
        diff_line = max_line_to_compare+1
    if diff_line == 0:
        return None
    def safeGetLine( lines, index ):
        index += -1
        if index >= len(lines):
            return ''
        return lines[index].strip()
    return """  Difference in %s at line %d:
  Expected: '%s'
  Actual:   '%s'
""" % (message, diff_line,
       safeGetLine(expected,diff_line),
       safeGetLine(actual,diff_line) )
        
def safeReadFile( path ):
    try:
        return file( path, 'rt' ).read()
    except IOError, e:
        return '<File "%s" is missing: %s>' % (path,e)

def runAllTests( jsontest_executable_path, input_dir = None ):
    if not input_dir:
        input_dir = os.getcwd()
    tests = glob( os.path.join( input_dir, '*.json' ) )
    if RUN_JSONCHECKER:
        test_jsonchecker = glob( os.path.join( input_dir, 'jsonchecker', '*.json' ) )
    else:
        test_jsonchecker = []
    failed_tests = []
    for input_path in tests + test_jsonchecker:
        is_json_checker_test = input_path in test_jsonchecker
        print 'TESTING:', input_path,
        options = is_json_checker_test and '--json-checker' or ''
        pipe = os.popen( "%s %s %s" % (jsontest_executable_path, options,
                                       input_path) )
        process_output = pipe.read()
        status = pipe.close()
        if is_json_checker_test:
            expect_failure = os.path.basename( input_path ).startswith( 'fail' )
            if expect_failure:
                if status is None:
                    print 'FAILED'
                    failed_tests.append( (input_path, 'Parsing should have failed:\n%s' %
                                          safeReadFile(input_path)) )
                else:
                    print 'OK'
            else:
                if status is not None:
                    print 'FAILED'
                    failed_tests.append( (input_path, 'Parsing failed:\n' + process_output) )
                else:
                    print 'OK'
        else:
            base_path = os.path.splitext(input_path)[0]
            actual_output = safeReadFile( base_path + '.actual' )
            actual_rewrite_output = safeReadFile( base_path + '.actual-rewrite' )
            file(base_path + '.process-output','wt').write( process_output )
            if status:
                print 'parsing failed'
                failed_tests.append( (input_path, 'Parsing failed:\n' + process_output) )
            else:
                expected_output_path = os.path.splitext(input_path)[0] + '.expected'
                expected_output = file( expected_output_path, 'rt' ).read()
                detail = ( compareOutputs( expected_output, actual_output, 'input' )
                            or compareOutputs( expected_output, actual_rewrite_output, 'rewrite' ) )
                if detail:
                    print 'FAILED'
                    failed_tests.append( (input_path, detail) )
                else:
                    print 'OK'

    if failed_tests:
        print
        print 'Failure details:'
        for failed_test in failed_tests:
            print '* Test', failed_test[0]
            print failed_test[1]
            print
        print 'Test results: %d passed, %d failed.' % (len(tests)-len(failed_tests),
                                                       len(failed_tests) )
        return 1
    else:
        print 'All %d tests passed.' % len(tests)
        return 0

if __name__ == '__main__':
    if len(sys.argv) < 1 or len(sys.argv) > 2:
        print "Usage: %s jsontest-executable-path [input-testcase-directory]" % sys.argv[0]
        sys.exit( 1 )

    jsontest_executable_path = os.path.normpath( os.path.abspath( sys.argv[1] ) )
    if len(sys.argv) > 2:
        input_path = os.path.normpath( os.path.abspath( sys.argv[2] ) )
    else:
        input_path = None
    status = runAllTests( jsontest_executable_path, input_path )
    sys.exit( status )