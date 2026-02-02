package cn.npdb.common;

import com.baomidou.mybatisplus.core.metadata.IPage;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PageResponse<T> {
    private List<T> records;
    private long page;
    private long pageSize;
    private long total;

    public static <T> PageResponse<T> from(IPage<T> page) {
        return new PageResponse<>(page.getRecords(), page.getCurrent(), page.getSize(), page.getTotal());
    }
}
