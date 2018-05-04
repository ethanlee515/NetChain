header_type netchain_t {
	fields {
		preamble : 64;
		type : 8;
		key : 32;
		value : 32;
		num_valid : 32;
	}
}


header_type port_t {
	fields {
		port_num : 8;
	}
}

header netchain_t netchain;

header port_t port;

register kv_store {
	width : 32;
	instance_count : 1000;
}

parser start {
	extract(netchain);
	extract(port);
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

action _route {
	modify_field(standard_metadata.egress_spec, port.port_num);
	remove_header(port);	
}

action _put {
	register_write(kv_store, netchain.key, netchain.value);
}

action _get {
	register_read(netchain.value, kv_store, netchain.key);
}


action _drop() {
	drop();
}

action _nop {}

table process {
	reads {
		netchain.preamble : exact;
		netchain.type : exact;
		netchain.key : exact;
	}
	actions {
		_put;
		_get;
		_nop;
	}
}

table route {
	reads {
		netchain.preamble : exact;
	}
	actions {
		_route;
		_drop;
	}
}

control ingress {

}

control egress {
	//empty
}

