import copy
import json
import sys


class Debugger:

    def __init__(self,source_code):

        self.source_code = source_code
        self.results = []
    def trace_func(self, frame, event, arg):
        if event == "line":

            locals_snapshot = copy.deepcopy(dict(frame.f_locals))

            self.results.append({
                "line": frame.f_lineno,
                "function": frame.f_code.co_name,
                "locals": locals_snapshot
            })


        return self.trace_func
    def run(self, arr):

        namespace = {}

        exec(self.source_code,namespace)

        function_name = next(name for name, obj in namespace.items()if callable(obj))

        target_function = namespace[function_name]

        sys.settrace(self.trace_func)

        try:

            target_function(arr)

            return {
                "date":self.results
            }
        finally:

            sys.settrace(   None )

if __name__=="__main__":
    source = '''
def merge_sort(arr):

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):

    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i] < right[j]:

            result.append(left[i])
            i += 1

        else:

            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result
    '''
    debugger = Debugger(
        source
    )

    response = debugger.run(
        [5, 3, 1, 4]
    )
    print(json.dumps(response, indent=4, ensure_ascii=False))