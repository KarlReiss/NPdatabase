package cn.npdb;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("cn.npdb.mapper")
public class NpdbApplication {
    public static void main(String[] args) {
        SpringApplication.run(NpdbApplication.class, args);
    }
}
