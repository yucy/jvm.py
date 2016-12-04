# -*- coding:utf-8 -*-
from common.utils import getDecimal


offset = 0
attr = []

def attrCursor(step):
	global offset
	# print '------attr',attr
	result = attr[offset:offset+step]
	offset += step
	return result

def parser(_attr):
	global attr
	attr = _attr
	attribute_name_index = attrCursor(2)
	name = content_pool[attribute_name_index]
	attribute_length = getDecimal(attrCursor(4))
	if attribute_length == 2:
		pass
	

'''
# one field type has this attrbute only one 
ConstantValue_attribute {
	u2 attribute_name_index;
	u4 attribute_length;# 值固定为2
	u2 constantvalue_index;
}

Code_attribute {
	u2 attribute_name_index;
	u4 attribute_length;
	u2 max_stack;
	u2 max_locals;
	u4 code_length;
	u1 code[code_length];
	u2 exception_table_length;
		{
		u2 start_pc;
		u2 end_pc;
		u2 handler_pc;
		u2 catch_type;
		} exception_table[exception_table_length];
	u2 attributes_count;
	attribute_info attributes[attributes_count];
}

StackMapTable_attribute {
	u2 attribute_name_index;
	u4 attribute_length;
	u2 number_of_entries;
	stack_map_frame entries[number_of_entries];
}

union stack_map_frame {
	same_frame;
	same_locals_1_stack_item_frame;
	same_locals_1_stack_item_frame_extended;
	chop_frame;
	same_frame_extended;
	append_frame;
	full_frame;
}


-----------------------------------------------------
field
ConstantValue(§4.7.2), Synthetic(§4.7.8), Signature(§4.7.9),
Deprecated(§4.7.15), RuntimeVisibleAnnotations(§4.7.16) 和
RuntimeInvisibleAnnotations(§4.7.17)
-----------------------------------------------------
method
Code(§4.7.3),
Exceptions(§4.7.5),Synthetic(§4.7.8),Signature(§4.7.9),
Deprecated(§4.7.15),untimeVisibleAnnotations(§4.7.16),
RuntimeInvisibleAnnotations(§4.7.17),
RuntimeVisibleParameterAnnotations(§4.7.18),
RuntimeInvisibleParameterAnnotations(§4.7.19)和
AnnotationDefault(§4.7.20)
-----------------------------------------------------
code
LineNumberTable
(§4.7.12),LocalVariableTable(§4.7.13),LocalVariableTypeTable
(§4.7.14)和 StackMapTable(§4.7.4)
-----------------------------------------------------

-----------------------------------------------------

-----------------------------------------------------
'''