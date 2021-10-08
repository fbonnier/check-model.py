# Error Handling


EXIT_SUCCESS = 0
EXIT_FAILURE = 1
error_msgs = {"continue":"\n----- Continue", "success":"\n----- Exit SUCCESS", "fail":"\n----- Exit FAIL"}

def print_error (error_msg, exit_type=None):
    print ((("Error :: ") if exit_type!="success" else "Message :: ") + str (error_msg) + ((" " + error_msgs[exit_type]) if exit_type!=None else ""))
