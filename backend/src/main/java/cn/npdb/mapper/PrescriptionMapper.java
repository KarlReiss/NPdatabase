package cn.npdb.mapper;

import cn.npdb.dto.PrescriptionListItem;
import cn.npdb.entity.Prescription;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

public interface PrescriptionMapper extends BaseMapper<Prescription> {
    @Select({
            "<script>",
            "SELECT",
            "  p.prescription_id AS prescriptionId,",
            "  p.chinese_name AS chineseName,",
            "  p.functions AS functions,",
            "  p.disease_icd11_category AS diseaseIcd11Category,",
            "  (",
            "    SELECT COUNT(DISTINCT pr.bio_resource_id)",
            "    FROM prescription_resources pr",
            "    WHERE pr.prescription_id = p.id",
            "  ) AS bioResourceCount",
            "FROM prescriptions p",
            "<if test='q != null and q != \"\"'>",
            "WHERE p.prescription_id ILIKE CONCAT('%', #{q}, '%')",
            "   OR p.chinese_name ILIKE CONCAT('%', #{q}, '%')",
            "   OR p.pinyin_name ILIKE CONCAT('%', #{q}, '%')",
            "</if>",
            "ORDER BY p.id DESC",
            "</script>"
    })
    Page<PrescriptionListItem> selectListPage(Page<?> page, @Param("q") String q);
}
