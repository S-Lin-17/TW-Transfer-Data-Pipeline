-- PostgreSQL table --

CREATE TABLE natural_gas_shipment (
    id SERIAL PRIMARY KEY,
    gas_date DATE NOT NULL,
    cycle_desc VARCHAR(10) NOT NULL,
    loc_code VARCHAR(6),
    loc_zone VARCHAR(50),
    loc_name VARCHAR(50),
    loc_purpose_desc VARCHAR(2),
    loc_qti VARCHAR(3),
    flow_ind VARCHAR(1),
    dc INT,
    opc INT,
    tsq INT,
    oac INT, -- oac = (opc - tsq)
    it VARCHAR(1),
    auth_overrun_ind VARCHAR(1),
    nom_cap_exceed_ind VARCHAR(1),
    all_qty_avail VARCHAR(1),
    qty_reason VARCHAR(50)
);