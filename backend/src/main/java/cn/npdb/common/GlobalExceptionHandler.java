package cn.npdb.common;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.validation.BindException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {
    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ApiResponse<Void> handleMethodArgumentNotValid(MethodArgumentNotValidException ex) {
        String message = ex.getBindingResult().getAllErrors().isEmpty()
                ? "Validation failed"
                : ex.getBindingResult().getAllErrors().get(0).getDefaultMessage();
        return ApiResponse.error(ApiCode.BAD_REQUEST, message);
    }

    @ExceptionHandler(BindException.class)
    public ApiResponse<Void> handleBindException(BindException ex) {
        String message = ex.getAllErrors().isEmpty()
                ? "Binding failed"
                : ex.getAllErrors().get(0).getDefaultMessage();
        return ApiResponse.error(ApiCode.BAD_REQUEST, message);
    }

//    @ExceptionHandler(ConstraintViolationException.class)
//    public ApiResponse<Void> handleConstraintViolation(ConstraintViolationException ex) {
//        return ApiResponse.error(ApiCode.BAD_REQUEST, ex.getMessage());
//    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ApiResponse<Void> handleIllegalArgument(IllegalArgumentException ex) {
        log.warn("Invalid argument: {}", ex.getMessage());
        return ApiResponse.error(ApiCode.BAD_REQUEST, ex.getMessage());
    }

    @ExceptionHandler(Exception.class)
    public ApiResponse<Void> handleException(Exception ex) {
        log.error("Unhandled exception", ex);
        String message = ex.getMessage() == null ? "Internal error" : ex.getMessage();
        return ApiResponse.error(ApiCode.INTERNAL_ERROR, message);
    }
}
