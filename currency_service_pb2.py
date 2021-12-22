# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: currency_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='currency_service.proto',
  package='finance_dashboard',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16\x63urrency_service.proto\x12\x11\x66inance_dashboard\"=\n\tTimeSlice\x12\r\n\x05start\x18\x01 \x01(\t\x12\x0b\n\x03\x65nd\x18\x02 \x01(\t\x12\x14\n\x0c\x63urrencyCode\x18\x03 \x01(\t\"\x16\n\x05Value\x12\r\n\x05value\x18\x01 \x01(\x02\x32]\n\x10\x43urrencyProvider\x12I\n\x0bGetCurrency\x12\x1c.finance_dashboard.TimeSlice\x1a\x18.finance_dashboard.Value\"\x00\x30\x01\x62\x06proto3'
)




_TIMESLICE = _descriptor.Descriptor(
  name='TimeSlice',
  full_name='finance_dashboard.TimeSlice',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='start', full_name='finance_dashboard.TimeSlice.start', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end', full_name='finance_dashboard.TimeSlice.end', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='currencyCode', full_name='finance_dashboard.TimeSlice.currencyCode', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=45,
  serialized_end=106,
)


_VALUE = _descriptor.Descriptor(
  name='Value',
  full_name='finance_dashboard.Value',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='finance_dashboard.Value.value', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=108,
  serialized_end=130,
)

DESCRIPTOR.message_types_by_name['TimeSlice'] = _TIMESLICE
DESCRIPTOR.message_types_by_name['Value'] = _VALUE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TimeSlice = _reflection.GeneratedProtocolMessageType('TimeSlice', (_message.Message,), {
  'DESCRIPTOR' : _TIMESLICE,
  '__module__' : 'currency_service_pb2'
  # @@protoc_insertion_point(class_scope:finance_dashboard.TimeSlice)
  })
_sym_db.RegisterMessage(TimeSlice)

Value = _reflection.GeneratedProtocolMessageType('Value', (_message.Message,), {
  'DESCRIPTOR' : _VALUE,
  '__module__' : 'currency_service_pb2'
  # @@protoc_insertion_point(class_scope:finance_dashboard.Value)
  })
_sym_db.RegisterMessage(Value)



_CURRENCYPROVIDER = _descriptor.ServiceDescriptor(
  name='CurrencyProvider',
  full_name='finance_dashboard.CurrencyProvider',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=132,
  serialized_end=225,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetCurrency',
    full_name='finance_dashboard.CurrencyProvider.GetCurrency',
    index=0,
    containing_service=None,
    input_type=_TIMESLICE,
    output_type=_VALUE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_CURRENCYPROVIDER)

DESCRIPTOR.services_by_name['CurrencyProvider'] = _CURRENCYPROVIDER

# @@protoc_insertion_point(module_scope)