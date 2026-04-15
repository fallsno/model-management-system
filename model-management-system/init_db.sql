-- 型号主表
CREATE TABLE model_families (
    id SERIAL PRIMARY KEY,
    family_code VARCHAR(50) NOT NULL UNIQUE,
    family_name VARCHAR(100),
    category VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 型号别名表
CREATE TABLE model_aliases (
    id SERIAL PRIMARY KEY,
    family_id INTEGER REFERENCES model_families(id) ON DELETE CASCADE,
    alias_code VARCHAR(50) NOT NULL,
    alias_type VARCHAR(20) DEFAULT 'old',
    is_primary BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(family_id, alias_code)
);

-- 型号版本表
CREATE TABLE model_versions (
    id SERIAL PRIMARY KEY,
    family_id INTEGER REFERENCES model_families(id) ON DELETE CASCADE,
    version_code VARCHAR(50) NOT NULL,
    specification TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(family_id, version_code)
);

-- 部件表
CREATE TABLE version_parts (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES model_versions(id) ON DELETE CASCADE,
    part_category VARCHAR(100) NOT NULL,
    part_name VARCHAR(200),
    part_code VARCHAR(50),
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 参数表
CREATE TABLE part_parameters (
    id SERIAL PRIMARY KEY,
    part_id INTEGER REFERENCES version_parts(id) ON DELETE CASCADE,
    param_name VARCHAR(100) NOT NULL,
    param_value TEXT,
    param_unit VARCHAR(50),
    param_type VARCHAR(20) DEFAULT 'text',
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 附件表
CREATE TABLE version_attachments (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES model_versions(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(100),
    file_size INTEGER,
    file_category VARCHAR(50),
    description TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    uploaded_by VARCHAR(100)
);

-- 搜索历史表
CREATE TABLE search_history (
    id SERIAL PRIMARY KEY,
    search_term VARCHAR(200) NOT NULL,
    search_count INTEGER DEFAULT 1,
    last_searched TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入初始型号数据
INSERT INTO model_families (family_code, family_name, category) VALUES
('AT240R.0', '干燥滚筒', '干燥滚筒'),
('RTS200.0', '顺流式再生滚筒', '再生滚筒'),
('HTS200.0', '逆流式再生滚筒', '再生滚筒'),
('CTD70G.0', '双回程干燥冷却滚筒', '干燥冷却滚筒'),
('CTS70G.0', '单回程干燥冷却滚筒', '干燥冷却滚筒'),
('MT500.0', '连续式干燥搅拌滚筒', '搅拌滚筒'),
('ST25100.0', '滚筒筛', '筛分设备'),
('WT200.0', '加湿筒', '加湿设备');

INSERT INTO model_aliases (family_id, alias_code, alias_type)
SELECT id, 'GT240GF1.0', 'old' FROM model_families WHERE family_code = 'AT240R.0'
UNION ALL SELECT id, 'GTRS200B.0', 'old' FROM model_families WHERE family_code = 'RTS200.0'
UNION ALL SELECT id, 'GTRQ200.0', 'old' FROM model_families WHERE family_code = 'HTS200.0'
UNION ALL SELECT id, 'GFT70Y.0', 'old' FROM model_families WHERE family_code = 'CTD70G.0'
UNION ALL SELECT id, 'GTL500A.0', 'old' FROM model_families WHERE family_code = 'MT500.0'
UNION ALL SELECT id, 'GTS25100.0', 'old' FROM model_families WHERE family_code = 'ST25100.0'
UNION ALL SELECT id, 'JSJ200A.0', 'old' FROM model_families WHERE family_code = 'WT200.0';