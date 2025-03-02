-- PostgreSQL table --

INSERT INTO natural_gas_shipment (
    gas_date,
    cycle_desc,
    loc_code,
    loc_zone,
    loc_name,
    loc_purpose_desc,
    loc_qti,
    flow_ind,
    dc,
    opc,
    tsq,
    oac,
    it,
    auth_overrun_ind,
    nom_cap_exceed_ind,
    all_qty_avail,
    qty_reason
) VALUES ( -- Placeholders, syntax uses $x -- 
    $1,
    $2,
    $3,
    $4,
    $5,
    $6,
    $7,
    $8,
    $9, 
    $10,
    $11,
    $12,
    $13,
    $14,
    $15,
    $16,
    $17
);