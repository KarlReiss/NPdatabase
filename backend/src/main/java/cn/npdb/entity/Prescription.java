package cn.npdb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@TableName("prescriptions")
public class Prescription {
    @TableId(type = IdType.AUTO)
    private Long id;

    private String prescriptionId;
    private String chineseName;
    private String pinyinName;
    private String englishName;

    private String functions;
    private String indications;

    private String tcmidId;
    private String diseaseIcd11Category;
    private String reference;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
