-- 创建 NPASS 结构数据表
CREATE TABLE IF NOT EXISTS npass_structures (
    id BIGSERIAL PRIMARY KEY,
    np_id VARCHAR(50) NOT NULL,
    inchi TEXT,
    inchikey VARCHAR(27),
    smiles TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引以提高查询性能
CREATE INDEX idx_npass_structures_np_id ON npass_structures(np_id);
CREATE INDEX idx_npass_structures_inchikey ON npass_structures(inchikey);

-- 添加注释
COMMENT ON TABLE npass_structures IS 'NPASS 3.0 天然产物结构数据';
COMMENT ON COLUMN npass_structures.np_id IS 'NPASS 天然产物 ID';
COMMENT ON COLUMN npass_structures.inchi IS 'InChI 标识符';
COMMENT ON COLUMN npass_structures.inchikey IS 'InChIKey 标识符';
COMMENT ON COLUMN npass_structures.smiles IS 'SMILES 结构式';
