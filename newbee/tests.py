dict_ = {"a": {"b": 1}}
return_data_form = dict_.get([k for k, v in dict_.items()][0])
print(return_data_form)