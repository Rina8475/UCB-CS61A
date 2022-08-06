(define (cddr s) (cdr (cdr s)))

(define (cadr s) (car (cdr s)))

(define (caddr s) (car (cdr (cdr s))))

(define (sign val)
    (cond ((< val 0) -1)
          ((> val 0) 1)
          (else 0)))

(define (square x) (* x x))

(define (pow base exp) 
    (define (pow-iter accumulator base exp)
        (cond ((= exp 0) accumulator)
              ((= (remainder exp 2) 0) 
                  (pow-iter accumulator (square base) (/ exp 2)))
              (else (pow-iter (* accumulator base) base (- exp 1))))
    )
    (pow-iter 1 base exp)
)
