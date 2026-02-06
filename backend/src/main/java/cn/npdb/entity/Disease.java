package cn.npdb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@TableName("diseases")
public class Disease {
    @TableId(type = IdType.AUTO)
    private Long id;

    private String icd11Code;
    private String diseaseName;
    private String diseaseNameZh;
    private String diseaseNameCmaup;
    private String diseaseCategory;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
