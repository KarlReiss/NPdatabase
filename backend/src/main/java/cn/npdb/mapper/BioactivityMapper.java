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
}
