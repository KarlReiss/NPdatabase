package cn.npdb.mapper;

import cn.npdb.dto.BioactivityTargetSummary;
import cn.npdb.dto.BioactivityWithNpId;
import cn.npdb.entity.Bioactivity;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

public interface BioactivityMapper extends BaseMapper<Bioactivity> {

    @Select("SELECT b.*, np.np_id FROM bioactivity b " +
            "JOIN natural_products np ON b.natural_product_id = np.id " +
            "WHERE b.target_id = #{targetDbId} ORDER BY b.id")
    Page<BioactivityWithNpId> listByTargetWithNpId(Page<BioactivityWithNpId> page, @Param("targetDbId") Long targetDbId);
    @Select(
            "SELECT " +
            "    t.id AS target_db_id, " +
            "    t.target_id AS target_id, " +
            "    t.target_name AS target_name, " +
            "    t.target_type AS target_type, " +
            "    t.target_organism AS target_organism, " +
            "    t.uniprot_id AS uniprot_id, " +
            "    COUNT(*) AS bioactivity_count, " +
            "    MIN(COALESCE(b.activity_value_std, b.activity_value)) AS best_activity_value " +
            "FROM bioactivity b " +
            "JOIN targets t ON b.target_id = t.id " +
            "WHERE b.natural_product_id = #{naturalProductId} " +
            "GROUP BY t.id, t.target_id, t.target_name, t.target_type, t.target_organism, t.uniprot_id " +
            "ORDER BY bioactivity_count DESC, t.target_id"
    )
    List<BioactivityTargetSummary> listTargetSummaries(@Param("naturalProductId") Long naturalProductId);

    @Select(
            "SELECT " +
            "    t.id AS target_db_id, " +
            "    t.target_id AS target_id, " +
            "    t.target_name AS target_name, " +
            "    t.target_type AS target_type, " +
            "    t.target_organism AS target_organism, " +
            "    t.uniprot_id AS uniprot_id, " +
            "    COUNT(*) AS bioactivity_count, " +
            "    MIN(COALESCE(b.activity_value_std, b.activity_value)) AS best_activity_value " +
            "FROM bioactivity b " +
            "JOIN targets t ON b.target_id = t.id " +
            "WHERE b.natural_product_id = #{naturalProductId} " +
            "GROUP BY t.id, t.target_id, t.target_name, t.target_type, t.target_organism, t.uniprot_id " +
            "ORDER BY bioactivity_count DESC, t.target_id"
    )
    Page<BioactivityTargetSummary> pageTargetSummaries(Page<BioactivityTargetSummary> page, @Param("naturalProductId") Long naturalProductId);

    @Select("SELECT b.id, b.natural_product_id, b.target_id AS target_db_id, " +
            "t.target_id, t.target_name, t.target_type, " +
            "b.activity_type, b.activity_type_grouped, b.activity_relation, " +
            "b.activity_value, b.activity_units, b.activity_value_std, b.activity_units_std, " +
            "b.assay_organism, b.assay_tax_id, b.assay_strain, b.assay_tissue, b.assay_cell_type, " +
            "b.ref_id, b.ref_id_type, b.created_at " +
            "FROM bioactivity b " +
            "LEFT JOIN targets t ON b.target_id = t.id " +
            "WHERE b.natural_product_id = #{naturalProductId} " +
            "ORDER BY b.id")
    Page<cn.npdb.dto.BioactivityWithTarget> pageByNaturalProductWithTarget(
            Page<cn.npdb.dto.BioactivityWithTarget> page,
            @Param("naturalProductId") Long naturalProductId);
}
