# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cai/pb/im/msg/service/comm_elem/comm_elem.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cai.pb.im.msg.msg_body import msg_body_pb2 as cai_dot_pb_dot_im_dot_msg_dot_msg__body_dot_msg__body__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/cai/pb/im/msg/service/comm_elem/comm_elem.proto\x12\x18im.msg.service.comm_elem\x1a%cai/pb/im/msg/msg_body/msg_body.proto\"\xfa\x01\n\x15MsgElemInfo_servtype1\x12\x11\n\treward_id\x18\x01 \x01(\x0c\x12\x12\n\nsender_uin\x18\x02 \x01(\x04\x12\x10\n\x08pic_type\x18\x03 \x01(\r\x12\x14\n\x0creward_money\x18\x04 \x01(\r\x12\x0b\n\x03url\x18\x05 \x01(\x0c\x12\x0f\n\x07\x63ontent\x18\x06 \x01(\x0c\x12\x18\n\x10\x63reate_timestamp\x18\x07 \x01(\r\x12\x0e\n\x06status\x18\x08 \x01(\r\x12\x0c\n\x04size\x18\t \x01(\r\x12\x16\n\x0evideo_duration\x18\n \x01(\r\x12\x0b\n\x03seq\x18\x0b \x01(\x04\x12\x17\n\x0freward_type_ext\x18\x0c \x01(\r\"\xc2\x01\n\x16MsgElemInfo_servtype11\x12\x0e\n\x06res_id\x18\x01 \x01(\x0c\x12\x0f\n\x07res_md5\x18\x02 \x01(\x0c\x12\x15\n\rreserve_info1\x18\x03 \x01(\x0c\x12\x15\n\rreserve_info2\x18\x04 \x01(\x0c\x12\x1a\n\x12\x64oodle_data_offset\x18\x05 \x01(\r\x12\x15\n\rdoodle_gif_id\x18\x06 \x01(\r\x12\x12\n\ndoodle_url\x18\x07 \x01(\x0c\x12\x12\n\ndoodle_md5\x18\x08 \x01(\x0c\"@\n\x16MsgElemInfo_servtype13\x12\x13\n\x0bsys_head_id\x18\x01 \x01(\r\x12\x11\n\thead_flag\x18\x02 \x01(\r\":\n\x16MsgElemInfo_servtype14\x12\n\n\x02id\x18\x01 \x01(\r\x12\x14\n\x0creserve_info\x18\x02 \x01(\x0c\"\xa7\x01\n\x16MsgElemInfo_servtype15\x12\x0b\n\x03vid\x18\x01 \x01(\x0c\x12\r\n\x05\x63over\x18\x02 \x01(\x0c\x12\r\n\x05title\x18\x03 \x01(\x0c\x12\x0f\n\x07summary\x18\x04 \x01(\x0c\x12\x13\n\x0b\x63reate_time\x18\x05 \x01(\x04\x12\x17\n\x0f\x63omment_content\x18\x06 \x01(\x0c\x12\x0e\n\x06\x61uthor\x18\x07 \x01(\x04\x12\x13\n\x0b\x63tr_version\x18\x08 \x01(\r\"\x8a\x02\n\x16MsgElemInfo_servtype16\x12\x0b\n\x03uid\x18\x01 \x01(\x04\x12\x10\n\x08union_id\x18\x02 \x01(\x0c\x12\x10\n\x08story_id\x18\x03 \x01(\x0c\x12\x0b\n\x03md5\x18\x04 \x01(\x0c\x12\x11\n\tthumb_url\x18\x05 \x01(\x0c\x12\x12\n\ndoodle_url\x18\x06 \x01(\x0c\x12\x13\n\x0bvideo_width\x18\x07 \x01(\r\x12\x14\n\x0cvideo_height\x18\x08 \x01(\r\x12\x13\n\x0bsource_name\x18\t \x01(\x0c\x12\x1a\n\x12source_action_type\x18\n \x01(\x0c\x12\x1a\n\x12source_action_data\x18\x0b \x01(\x0c\x12\x13\n\x0b\x63tr_version\x18\x0c \x01(\r\"x\n\x16MsgElemInfo_servtype18\x12\x16\n\x0e\x63urrent_amount\x18\x01 \x01(\x04\x12\x14\n\x0ctotal_amount\x18\x02 \x01(\x04\x12\x0e\n\x06listid\x18\x03 \x01(\x0c\x12\x10\n\x08\x61uth_key\x18\x04 \x01(\x0c\x12\x0e\n\x06number\x18\x05 \x01(\r\"&\n\x16MsgElemInfo_servtype19\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\"\xed\x01\n\x15MsgElemInfo_servtype2\x12\x11\n\tpoke_type\x18\x01 \x01(\r\x12\x14\n\x0cpoke_summary\x18\x02 \x01(\x0c\x12\x12\n\ndouble_hit\x18\x03 \x01(\r\x12\x12\n\nvaspoke_id\x18\x04 \x01(\r\x12\x14\n\x0cvaspoke_name\x18\x05 \x01(\x0c\x12\x16\n\x0evaspoke_minver\x18\x06 \x01(\x0c\x12\x15\n\rpoke_strength\x18\x07 \x01(\r\x12\x10\n\x08msg_type\x18\x08 \x01(\r\x12\x19\n\x11\x66\x61\x63\x65_bubble_count\x18\t \x01(\r\x12\x11\n\tpoke_flag\x18\n \x01(\r\"&\n\x16MsgElemInfo_servtype20\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\"\x81\x03\n\x16MsgElemInfo_servtype21\x12\x10\n\x08topic_id\x18\x01 \x01(\r\x12\x15\n\rconfessor_uin\x18\x02 \x01(\x04\x12\x16\n\x0e\x63onfessor_nick\x18\x03 \x01(\x0c\x12\x15\n\rconfessor_sex\x18\x04 \x01(\r\x12\x13\n\x0bsysmsg_flag\x18\x05 \x01(\r\x12\x45\n\x10\x63\x32_c_confess_ctx\x18\x06 \x01(\x0b\x32+.im.msg.service.comm_elem.C2CConfessContext\x12\r\n\x05topic\x18\x07 \x01(\x0c\x12\x14\n\x0c\x63onfess_time\x18\x08 \x01(\x04\x12\x44\n\x11group_confess_msg\x18\t \x01(\x0b\x32).im.msg.service.comm_elem.GroupConfessMsg\x12H\n\x11group_confess_ctx\x18\n \x01(\x0b\x32-.im.msg.service.comm_elem.GroupConfessContext\"\x8c\x02\n\x11\x43\x32\x43\x43onfessContext\x12\x15\n\rconfessor_uin\x18\x01 \x01(\x04\x12\x16\n\x0e\x63onfess_to_uin\x18\x02 \x01(\x04\x12\x10\n\x08send_uin\x18\x03 \x01(\x04\x12\x16\n\x0e\x63onfessor_nick\x18\x04 \x01(\x0c\x12\x0f\n\x07\x63onfess\x18\x05 \x01(\x0c\x12\x0f\n\x07\x62g_type\x18\x06 \x01(\r\x12\x10\n\x08topic_id\x18\x07 \x01(\r\x12\x14\n\x0c\x63onfess_time\x18\x08 \x01(\x04\x12\x15\n\rconfessor_sex\x18\t \x01(\r\x12\x10\n\x08\x62iz_type\x18\n \x01(\r\x12\x13\n\x0b\x63onfess_num\x18\x0b \x01(\r\x12\x16\n\x0e\x63onfess_to_sex\x18\x0c \x01(\r\"\xf3\x01\n\x13GroupConfessContext\x12\x15\n\rconfessor_uin\x18\x01 \x01(\x04\x12\x16\n\x0e\x63onfess_to_uin\x18\x02 \x01(\x04\x12\x10\n\x08send_uin\x18\x03 \x01(\x04\x12\x15\n\rconfessor_sex\x18\x04 \x01(\r\x12\x17\n\x0f\x63onfess_to_nick\x18\x05 \x01(\x0c\x12\r\n\x05topic\x18\x06 \x01(\x0c\x12\x10\n\x08topic_id\x18\x07 \x01(\r\x12\x14\n\x0c\x63onfess_time\x18\x08 \x01(\x04\x12\x1c\n\x14\x63onfess_to_nick_type\x18\t \x01(\r\x12\x16\n\x0e\x63onfessor_nick\x18\n \x01(\x0c\"\x82\x01\n\x10GroupConfessItem\x12\x10\n\x08topic_id\x18\x01 \x01(\r\x12\x16\n\x0e\x63onfess_to_uin\x18\x02 \x01(\x04\x12\x17\n\x0f\x63onfess_to_nick\x18\x03 \x01(\x0c\x12\r\n\x05topic\x18\x04 \x01(\x0c\x12\x1c\n\x14\x63onfess_to_nick_type\x18\x05 \x01(\r\"\xc8\x01\n\x0fGroupConfessMsg\x12\x14\n\x0c\x63onfess_time\x18\x01 \x01(\x04\x12\x15\n\rconfessor_uin\x18\x02 \x01(\x04\x12\x15\n\rconfessor_sex\x18\x03 \x01(\r\x12\x13\n\x0bsysmsg_flag\x18\x04 \x01(\r\x12\x41\n\rconfess_items\x18\x05 \x03(\x0b\x32*.im.msg.service.comm_elem.GroupConfessItem\x12\x19\n\x11total_topic_count\x18\x06 \x01(\r\"\xc1\x01\n\x16MsgElemInfo_servtype23\x12\x11\n\tface_type\x18\x01 \x01(\r\x12\x19\n\x11\x66\x61\x63\x65_bubble_count\x18\x02 \x01(\r\x12\x14\n\x0c\x66\x61\x63\x65_summary\x18\x03 \x01(\x0c\x12\x0c\n\x04\x66lag\x18\x04 \x01(\r\x12\x0e\n\x06others\x18\x05 \x01(\x0c\x12\x45\n\x0byellow_face\x18\x06 \x01(\x0b\x32\x30.im.msg.service.comm_elem.MsgElemInfo_servtype33\"\x9e\x01\n\x16MsgElemInfo_servtype24\x12\x42\n\x10limit_chat_enter\x18\x01 \x01(\x0b\x32(.im.msg.service.comm_elem.LimitChatEnter\x12@\n\x0flimit_chat_exit\x18\x02 \x01(\x0b\x32\'.im.msg.service.comm_elem.LimitChatExit\"\xad\x01\n\x0eLimitChatEnter\x12\x14\n\x0ctips_wording\x18\x01 \x01(\x0c\x12\x16\n\x0eleft_chat_time\x18\x02 \x01(\r\x12\x10\n\x08match_ts\x18\x03 \x01(\x04\x12\x1a\n\x12match_expired_time\x18\x04 \x01(\r\x12\x19\n\x11\x63\x32_c_expired_time\x18\x05 \x01(\r\x12\x10\n\x08ready_ts\x18\x06 \x01(\x04\x12\x12\n\nmatch_nick\x18\x07 \x01(\x0c\"6\n\rLimitChatExit\x12\x13\n\x0b\x65xit_method\x18\x01 \x01(\r\x12\x10\n\x08match_ts\x18\x02 \x01(\x04\"H\n\x16MsgElemInfo_servtype27\x12.\n\nvideo_file\x18\x01 \x01(\x0b\x32\x1a.im.msg.msg_body.VideoFile\".\n\x16MsgElemInfo_servtype29\x12\x14\n\x0cluckybag_msg\x18\x01 \x01(\x0c\"\x86\x01\n\x15MsgElemInfo_servtype3\x12\x34\n\x0f\x66lash_troop_pic\x18\x01 \x01(\x0b\x32\x1b.im.msg.msg_body.CustomFace\x12\x37\n\x0e\x66lash_c2_c_pic\x18\x02 \x01(\x0b\x32\x1f.im.msg.msg_body.NotOnlineImage\"3\n\x16MsgElemInfo_servtype31\x12\x0c\n\x04text\x18\x01 \x01(\x0c\x12\x0b\n\x03\x65xt\x18\x02 \x01(\x0c\"R\n\x16MsgElemInfo_servtype33\x12\r\n\x05index\x18\x01 \x01(\r\x12\x0c\n\x04text\x18\x02 \x01(\x0c\x12\x0e\n\x06\x63ompat\x18\x03 \x01(\x0c\x12\x0b\n\x03\x62uf\x18\x04 \x01(\x0c\"\x93\x01\n\x16MsgElemInfo_servtype34\x12\x15\n\rfrom_nickname\x18\x01 \x01(\x0c\x12\x18\n\x10push_window_flag\x18\x02 \x01(\r\x12;\n\x0cgame_session\x18\x03 \x01(\x0b\x32%.im.msg.service.comm_elem.GameSession\x12\x0b\n\x03\x65xt\x18\x04 \x01(\x0c\"\x9f\x01\n\x0bGameSession\x12\x14\n\x0c\x66rom_role_id\x18\x01 \x01(\x0c\x12\x14\n\x0c\x66rom_open_id\x18\x02 \x01(\x0c\x12\x12\n\nto_role_id\x18\x03 \x01(\x0c\x12\x12\n\nto_open_id\x18\x04 \x01(\x0c\x12\x12\n\ngame_appid\x18\x05 \x01(\x04\x12\x14\n\x0c\x66rom_tiny_id\x18\x06 \x01(\x04\x12\x12\n\nto_tiny_id\x18\x07 \x01(\x04\"h\n\x16MsgElemInfo_servtype35\x12\r\n\x05token\x18\x01 \x01(\x0c\x12\x14\n\x0cglobal_padid\x18\x02 \x01(\x0c\x12\x0f\n\x07get_rev\x18\x03 \x01(\r\x12\x18\n\x10his_edit_uin_num\x18\x04 \x01(\r\"r\n\x15MsgElemInfo_servtype4\x12\x11\n\timsg_type\x18\x01 \x01(\r\x12\x46\n\x14st_story_aio_obj_msg\x18\x04 \x01(\x0b\x32(.im.msg.service.comm_elem.StoryAioObjMsg\"\x91\x01\n\x15MsgElemInfo_servtype5\x12\x0b\n\x03vid\x18\x01 \x01(\x0c\x12\r\n\x05\x63over\x18\x02 \x01(\x0c\x12\r\n\x05title\x18\x03 \x01(\x0c\x12\x0f\n\x07summary\x18\x04 \x01(\x0c\x12\x13\n\x0b\x63reate_time\x18\x05 \x01(\x04\x12\x17\n\x0f\x63omment_content\x18\x06 \x01(\x0c\x12\x0e\n\x06\x61uthor\x18\x07 \x01(\x04\"W\n\x15MsgElemInfo_servtype8\x12>\n\x15wifi_deliver_gift_msg\x18\x01 \x01(\x0b\x32\x1f.im.msg.msg_body.DeliverGiftMsg\"\x89\x01\n\x15MsgElemInfo_servtype9\x12\x15\n\ranchor_status\x18\x01 \x01(\r\x12\x13\n\x0bjump_schema\x18\x02 \x01(\x0c\x12\x17\n\x0f\x61nchor_nickname\x18\x03 \x01(\t\x12\x17\n\x0f\x61nchor_head_url\x18\x04 \x01(\x0c\x12\x12\n\nlive_title\x18\x05 \x01(\t\"1\n\x0eStoryAioObjMsg\x12\x0e\n\x06ui_url\x18\x01 \x01(\t\x12\x0f\n\x07jmp_url\x18\x02 \x01(\t')



_MSGELEMINFO_SERVTYPE1 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype1']
_MSGELEMINFO_SERVTYPE11 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype11']
_MSGELEMINFO_SERVTYPE13 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype13']
_MSGELEMINFO_SERVTYPE14 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype14']
_MSGELEMINFO_SERVTYPE15 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype15']
_MSGELEMINFO_SERVTYPE16 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype16']
_MSGELEMINFO_SERVTYPE18 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype18']
_MSGELEMINFO_SERVTYPE19 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype19']
_MSGELEMINFO_SERVTYPE2 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype2']
_MSGELEMINFO_SERVTYPE20 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype20']
_MSGELEMINFO_SERVTYPE21 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype21']
_C2CCONFESSCONTEXT = DESCRIPTOR.message_types_by_name['C2CConfessContext']
_GROUPCONFESSCONTEXT = DESCRIPTOR.message_types_by_name['GroupConfessContext']
_GROUPCONFESSITEM = DESCRIPTOR.message_types_by_name['GroupConfessItem']
_GROUPCONFESSMSG = DESCRIPTOR.message_types_by_name['GroupConfessMsg']
_MSGELEMINFO_SERVTYPE23 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype23']
_MSGELEMINFO_SERVTYPE24 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype24']
_LIMITCHATENTER = DESCRIPTOR.message_types_by_name['LimitChatEnter']
_LIMITCHATEXIT = DESCRIPTOR.message_types_by_name['LimitChatExit']
_MSGELEMINFO_SERVTYPE27 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype27']
_MSGELEMINFO_SERVTYPE29 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype29']
_MSGELEMINFO_SERVTYPE3 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype3']
_MSGELEMINFO_SERVTYPE31 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype31']
_MSGELEMINFO_SERVTYPE33 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype33']
_MSGELEMINFO_SERVTYPE34 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype34']
_GAMESESSION = DESCRIPTOR.message_types_by_name['GameSession']
_MSGELEMINFO_SERVTYPE35 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype35']
_MSGELEMINFO_SERVTYPE4 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype4']
_MSGELEMINFO_SERVTYPE5 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype5']
_MSGELEMINFO_SERVTYPE8 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype8']
_MSGELEMINFO_SERVTYPE9 = DESCRIPTOR.message_types_by_name['MsgElemInfo_servtype9']
_STORYAIOOBJMSG = DESCRIPTOR.message_types_by_name['StoryAioObjMsg']
MsgElemInfo_servtype1 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype1', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE1,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype1)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype1)

MsgElemInfo_servtype11 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype11', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE11,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype11)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype11)

MsgElemInfo_servtype13 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype13', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE13,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype13)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype13)

MsgElemInfo_servtype14 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype14', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE14,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype14)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype14)

MsgElemInfo_servtype15 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype15', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE15,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype15)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype15)

MsgElemInfo_servtype16 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype16', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE16,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype16)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype16)

MsgElemInfo_servtype18 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype18', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE18,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype18)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype18)

MsgElemInfo_servtype19 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype19', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE19,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype19)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype19)

MsgElemInfo_servtype2 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype2', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE2,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype2)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype2)

MsgElemInfo_servtype20 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype20', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE20,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype20)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype20)

MsgElemInfo_servtype21 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype21', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE21,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype21)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype21)

C2CConfessContext = _reflection.GeneratedProtocolMessageType('C2CConfessContext', (_message.Message,), {
  'DESCRIPTOR' : _C2CCONFESSCONTEXT,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.C2CConfessContext)
  })
_sym_db.RegisterMessage(C2CConfessContext)

GroupConfessContext = _reflection.GeneratedProtocolMessageType('GroupConfessContext', (_message.Message,), {
  'DESCRIPTOR' : _GROUPCONFESSCONTEXT,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.GroupConfessContext)
  })
_sym_db.RegisterMessage(GroupConfessContext)

GroupConfessItem = _reflection.GeneratedProtocolMessageType('GroupConfessItem', (_message.Message,), {
  'DESCRIPTOR' : _GROUPCONFESSITEM,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.GroupConfessItem)
  })
_sym_db.RegisterMessage(GroupConfessItem)

GroupConfessMsg = _reflection.GeneratedProtocolMessageType('GroupConfessMsg', (_message.Message,), {
  'DESCRIPTOR' : _GROUPCONFESSMSG,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.GroupConfessMsg)
  })
_sym_db.RegisterMessage(GroupConfessMsg)

MsgElemInfo_servtype23 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype23', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE23,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype23)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype23)

MsgElemInfo_servtype24 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype24', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE24,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype24)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype24)

LimitChatEnter = _reflection.GeneratedProtocolMessageType('LimitChatEnter', (_message.Message,), {
  'DESCRIPTOR' : _LIMITCHATENTER,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.LimitChatEnter)
  })
_sym_db.RegisterMessage(LimitChatEnter)

LimitChatExit = _reflection.GeneratedProtocolMessageType('LimitChatExit', (_message.Message,), {
  'DESCRIPTOR' : _LIMITCHATEXIT,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.LimitChatExit)
  })
_sym_db.RegisterMessage(LimitChatExit)

MsgElemInfo_servtype27 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype27', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE27,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype27)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype27)

MsgElemInfo_servtype29 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype29', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE29,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype29)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype29)

MsgElemInfo_servtype3 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype3', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE3,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype3)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype3)

MsgElemInfo_servtype31 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype31', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE31,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype31)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype31)

MsgElemInfo_servtype33 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype33', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE33,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype33)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype33)

MsgElemInfo_servtype34 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype34', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE34,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype34)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype34)

GameSession = _reflection.GeneratedProtocolMessageType('GameSession', (_message.Message,), {
  'DESCRIPTOR' : _GAMESESSION,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.GameSession)
  })
_sym_db.RegisterMessage(GameSession)

MsgElemInfo_servtype35 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype35', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE35,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype35)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype35)

MsgElemInfo_servtype4 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype4', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE4,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype4)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype4)

MsgElemInfo_servtype5 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype5', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE5,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype5)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype5)

MsgElemInfo_servtype8 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype8', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE8,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype8)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype8)

MsgElemInfo_servtype9 = _reflection.GeneratedProtocolMessageType('MsgElemInfo_servtype9', (_message.Message,), {
  'DESCRIPTOR' : _MSGELEMINFO_SERVTYPE9,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.MsgElemInfo_servtype9)
  })
_sym_db.RegisterMessage(MsgElemInfo_servtype9)

StoryAioObjMsg = _reflection.GeneratedProtocolMessageType('StoryAioObjMsg', (_message.Message,), {
  'DESCRIPTOR' : _STORYAIOOBJMSG,
  '__module__' : 'cai.pb.im.msg.service.comm_elem.comm_elem_pb2'
  # @@protoc_insertion_point(class_scope:im.msg.service.comm_elem.StoryAioObjMsg)
  })
_sym_db.RegisterMessage(StoryAioObjMsg)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MSGELEMINFO_SERVTYPE1._serialized_start=117
  _MSGELEMINFO_SERVTYPE1._serialized_end=367
  _MSGELEMINFO_SERVTYPE11._serialized_start=370
  _MSGELEMINFO_SERVTYPE11._serialized_end=564
  _MSGELEMINFO_SERVTYPE13._serialized_start=566
  _MSGELEMINFO_SERVTYPE13._serialized_end=630
  _MSGELEMINFO_SERVTYPE14._serialized_start=632
  _MSGELEMINFO_SERVTYPE14._serialized_end=690
  _MSGELEMINFO_SERVTYPE15._serialized_start=693
  _MSGELEMINFO_SERVTYPE15._serialized_end=860
  _MSGELEMINFO_SERVTYPE16._serialized_start=863
  _MSGELEMINFO_SERVTYPE16._serialized_end=1129
  _MSGELEMINFO_SERVTYPE18._serialized_start=1131
  _MSGELEMINFO_SERVTYPE18._serialized_end=1251
  _MSGELEMINFO_SERVTYPE19._serialized_start=1253
  _MSGELEMINFO_SERVTYPE19._serialized_end=1291
  _MSGELEMINFO_SERVTYPE2._serialized_start=1294
  _MSGELEMINFO_SERVTYPE2._serialized_end=1531
  _MSGELEMINFO_SERVTYPE20._serialized_start=1533
  _MSGELEMINFO_SERVTYPE20._serialized_end=1571
  _MSGELEMINFO_SERVTYPE21._serialized_start=1574
  _MSGELEMINFO_SERVTYPE21._serialized_end=1959
  _C2CCONFESSCONTEXT._serialized_start=1962
  _C2CCONFESSCONTEXT._serialized_end=2230
  _GROUPCONFESSCONTEXT._serialized_start=2233
  _GROUPCONFESSCONTEXT._serialized_end=2476
  _GROUPCONFESSITEM._serialized_start=2479
  _GROUPCONFESSITEM._serialized_end=2609
  _GROUPCONFESSMSG._serialized_start=2612
  _GROUPCONFESSMSG._serialized_end=2812
  _MSGELEMINFO_SERVTYPE23._serialized_start=2815
  _MSGELEMINFO_SERVTYPE23._serialized_end=3008
  _MSGELEMINFO_SERVTYPE24._serialized_start=3011
  _MSGELEMINFO_SERVTYPE24._serialized_end=3169
  _LIMITCHATENTER._serialized_start=3172
  _LIMITCHATENTER._serialized_end=3345
  _LIMITCHATEXIT._serialized_start=3347
  _LIMITCHATEXIT._serialized_end=3401
  _MSGELEMINFO_SERVTYPE27._serialized_start=3403
  _MSGELEMINFO_SERVTYPE27._serialized_end=3475
  _MSGELEMINFO_SERVTYPE29._serialized_start=3477
  _MSGELEMINFO_SERVTYPE29._serialized_end=3523
  _MSGELEMINFO_SERVTYPE3._serialized_start=3526
  _MSGELEMINFO_SERVTYPE3._serialized_end=3660
  _MSGELEMINFO_SERVTYPE31._serialized_start=3662
  _MSGELEMINFO_SERVTYPE31._serialized_end=3713
  _MSGELEMINFO_SERVTYPE33._serialized_start=3715
  _MSGELEMINFO_SERVTYPE33._serialized_end=3797
  _MSGELEMINFO_SERVTYPE34._serialized_start=3800
  _MSGELEMINFO_SERVTYPE34._serialized_end=3947
  _GAMESESSION._serialized_start=3950
  _GAMESESSION._serialized_end=4109
  _MSGELEMINFO_SERVTYPE35._serialized_start=4111
  _MSGELEMINFO_SERVTYPE35._serialized_end=4215
  _MSGELEMINFO_SERVTYPE4._serialized_start=4217
  _MSGELEMINFO_SERVTYPE4._serialized_end=4331
  _MSGELEMINFO_SERVTYPE5._serialized_start=4334
  _MSGELEMINFO_SERVTYPE5._serialized_end=4479
  _MSGELEMINFO_SERVTYPE8._serialized_start=4481
  _MSGELEMINFO_SERVTYPE8._serialized_end=4568
  _MSGELEMINFO_SERVTYPE9._serialized_start=4571
  _MSGELEMINFO_SERVTYPE9._serialized_end=4708
  _STORYAIOOBJMSG._serialized_start=4710
  _STORYAIOOBJMSG._serialized_end=4759
# @@protoc_insertion_point(module_scope)
