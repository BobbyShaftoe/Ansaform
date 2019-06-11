import junit_xml_output
test_cases = []
test_cases.append(junit_xml_output.TestCase("first", "eg_contents",
    "failure"))
junit_xml = junit_xml_output.JunitXml("example_usage", test_cases)
print (junit_xml.dump())


# 
# # code snippet for the usage
# """ a short example of how to use this module """
# test_cases = []
# for i in range(0, 5):
#     type_c = ""
#     if i % 2 == 0:
#         type_c = "failure"
#     test_cases.append(TestCase(i, str(i) + "contents", type_c) )
# 
# junit_xml = JunitXml("demo test example", test_cases)
