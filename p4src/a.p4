header_type easyroute_t {
	fields {
		preamble : 64;
		num_valid : 32;
	}
}

header_type port_t {
	fields {
		port_num : 8;
	}
}

header easyroute_t easyroute;
header port_t port;

parser start {
	extract(easyroute);
	extract(port);
	return ingress;
}

table check_easyroute {
	reads {
		easyroute.preamble : exact;
	}
	actions {
		_no_op;
		_drop;
	}
}

table check_num_valid {
	reads {
		easyroute.num_valid : exact;
	}
	actions {
		route;
		_drop;
	}
}

action route() {
	modify_field(standard_metadata.egress_spec, port.port_num);
	subtract_from_field(easyroute.num_valid, 1);
	remove_header(port);
}

action _no_op() {

}

action _drop() {
	drop();
}

control ingress {
	apply(check_num_valid);
	apply(check_easyroute);
}

control egress {
    // leave empty
}
