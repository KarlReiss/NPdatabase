package cn.npdb.mapper;

import cn.npdb.entity.Disease;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

public interface DiseaseMapper extends BaseMapper<Disease> {
    @Select({
            "<script>",
            "SELECT",
            "  d.id AS id,",
            "  d.icd11_code AS icd11Code,",
            "  d.disease_name AS diseaseName,",
            "  d.disease_name_zh AS diseaseNameZh,",
            "  d.disease_name_cmaup AS diseaseNameCmaup,",
            "  d.disease_category AS diseaseCategory,",
            "  d.created_at AS createdAt,",
            "  d.updated_at AS updatedAt",
            "FROM diseases d",
            "<where>",
            "  <if test='q != null and q != \"\"'>",
            "    (d.disease_name ILIKE CONCAT('%', #{q}, '%')",
            "     OR d.disease_name_zh ILIKE CONCAT('%', #{q}, '%')",
            "     OR d.disease_name_cmaup ILIKE CONCAT('%', #{q}, '%')",
            "     OR d.icd11_code ILIKE CONCAT('%', #{q}, '%'))",
            "  </if>",
            "  <if test='category != null and category != \"\"'>",
            "    <if test='q != null and q != \"\"'>",
            "      AND",
            "    </if>",
            "    d.disease_category = #{category}",
            "  </if>",
            "</where>",
            "ORDER BY d.id DESC",
            "</script>"
    })
    Page<Disease> selectListPage(Page<?> page, @Param("q") String q, @Param("category") String category);
}
