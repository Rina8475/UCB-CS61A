(define (tail-replicate x n)
    (define (tail-iter accumulator n)
        (if (= n 0) accumulator
            (tail-iter (cons x accumulator) (- n 1))))
    (tail-iter '() n)
)

(define-macro (def func args body)
  `(define ,func
       (lambda ,args ,body)))

(define (repeatedly-cube n x)
  (if (zero? n)
      x
      (let ((y (repeatedly-cube (- n 1) x)))
        (* y y y))))
