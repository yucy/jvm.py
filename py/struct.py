CONSTANT_Class_info = {
	#u1 tag
	'tag':1,
	#u2 name_index
	'name_index': 2,
}

CONSTANT_Fieldref_info = {
	#u1  tag
	'tag':1,
	#u2  class_index
	'class_index':2,
	#u2  name_and_type_index
	'name_and_type_index':2,
}

CONSTANT_Methodref_info = {
	#u1  tag
	'tag':1,
	#u2  class_index
	'class_index':2,
	#u2  name_and_type_index
	'name_and_type_index':2,
}

CONSTANT_InterfaceMethodref_info = {
	#u1  tag
	'tag':1,
	#u2  class_index
	'class_index':2,
	#u2  name_and_type_index
	'name_and_type_index':2,
}

CONSTANT_String_info = {
	#u1  tag
	'tag':1,
	#u2  string_index
	'string_index':2,
}

CONSTANT_Integer_info = {
	#u1  tag
	'tag':1,
	#u4  bytes
	'bytes':4,
}

CONSTANT_Float_info = {
	#u1  tag
	'tag':1,
	#u4  bytes
	'bytes':4,
}

CONSTANT_Long_info = {
	#u1  tag
	'tag':1,
	#u4  high_bytes
	'high_bytes':4,
	#u4  low_bytes
	'low_bytes':4,
}

CONSTANT_Double_info = {
	#u1  tag
	'tag':1,
	#u4  high_bytes
	'high_bytes':4,
	#u4  low_bytes
	'low_bytes':4,
}

CONSTANT_NameAndType_info = {
	#u1  tag
	'tag':1,
	#u2  name_index
	'name_index':2,
	#u2  descriptor_index
	'descriptor_index':2,
}

CONSTANT_Utf8_info = {
	#u1  tag
	'tag':1,
	#u2  length
	'length':2,
	#u1  bytes[length]
	'bytes':1,
}

CONSTANT_MethodHandle_info = {
	#u1  tag
	'tag':1,
	#u1  reference_kind
	'reference_kind':1,
	#u2  reference_index
	'reference_index':2,
}

CONSTANT_MethodType_info = {
	#u1  tag
	'tag':1,
	#u2  descriptor_index
	'descriptor_index':2,
}

CONSTANT_InvokeDynamic_info = {
	#u1  tag
	'tag':1,
	#u2  bootstrap_method_attr_index
	'bootstrap_method_attr_index':2,
	#u2  name_and_type_index
	'name_and_type_index':2,
}