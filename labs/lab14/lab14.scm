(define (split-at lst n)
    (cond ((or (equal? lst nil) (= n 0)) `(() ,@lst))
          (#t (let ((result (split-at (cdr lst) (- n 1))))
                   (cons (cons (car lst) (car result))
                         (cdr result)))))    
)

(define (compose-all funcs)
    (define (compose-all-iter accu-func funcs)
        (if (equal? funcs nil) accu-func
            (compose-all-iter (lambda (x) ((car funcs) (accu-func x)))
                              (cdr funcs))))
    (compose-all-iter (lambda (x) x) funcs)
)