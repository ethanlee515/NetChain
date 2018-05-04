header_type keyvalue_t {
	fields {
		preamble : 64;
		unused : 40;
		mtype : 8;
		key : 32;
		value : 32;
	}
}

header keyvalue_t keyvalue;

register kv_store {
	width : 32;
	instance_count : 1000;
}

parser start {
    extract(keyvalue);
    return ingress;
}

table check_mtype {
	reads {
		keyvalue.preamble : exact;
		keyvalue.mtype : exact;
	}
	actions {
		put;
		get;
		_drop;
	}
}

action put() {
	modify_field(standard_metadata.egress_spec, standard_metadata.ingress_port);
	modify_field(keyvalue.mtype, 3);
	register_write(kv_store, keyvalue.key, keyvalue.value);
}

action get() {
	modify_field(standard_metadata.egress_spec, standard_metadata.ingress_port);
	modify_field(keyvalue.mtype, 2);
	register_read(keyvalue.value, kv_store, keyvalue.key);
}

action _drop() {
	drop();
}

control ingress {
	apply(check_mtype);
}

control egress {
    // leave empty
}
