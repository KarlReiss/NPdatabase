package cn.npdb.service;

import cn.npdb.dto.PrescriptionListItem;
import cn.npdb.entity.Prescription;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;

public interface PrescriptionService extends IService<Prescription> {
    Page<PrescriptionListItem> listPage(Page<?> page, String q);
}
