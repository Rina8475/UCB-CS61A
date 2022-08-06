;;;;;;;;;;;;;;;;;;;; Q1 ;;;;;;;;;;;;;;;;;
; ? Part A
; ! Difficulty *
(define (skip n lst)
    (if (or (= n 0) (equal? lst nil))
        lst
        (skip (- n 1) (cdr lst))
    )
)

(expect (skip 2 '(1 2 3 4)) (3 4))

(expect (skip 10 '(1 2 3 4)) ())

; ? Part B
; ! Difficulty ***
(define (infix expr)
    (cond 
        ((not (pair? expr)) (eval expr))
        ((null? (cdr expr)) (infix (car expr)))
        (else
            (define left (car expr))
            (define right (cdr (cdr expr)))
            (define operator (car (cdr expr)))
            (cond 
                ((equal? operator '+)
                    (+ (infix left) (infix right))
                )
                ((equal? operator '*)
                    (infix (cons (* (infix left) (infix (car right)))
                                 (cdr right))
                    )
                )
            )
        )
    )
)

(expect (infix '(1 + 2)) 3)

(expect (infix '(1 * 2)) 2)

(expect (infix '(3 + 2 * 5 + 4)) 17)

(expect (infix '(1 + 2 * (3 + 4))) 15)

(expect (infix '(1 + 2 * (3 + 4 * (5 + 6)))) 95)

(expect (infix '(1 + (2 + 3))) 6)

(define x 3)

(expect (infix '(x + 2)) 5)

(expect (infix '(1 * x)) 3)

(expect (infix '((x + x) * (x + x))) 36)




;;;;;;;;;;;;;;;;;;;; Q2 ;;;;;;;;;;;;;;;;;
; ! Difficulty ***
(define (nondecreaselist s)
    (if (equal? s nil)
        nil
        (let ((rest (nondecreaselist (cdr s))))
            (if (or (equal? rest nil) (> (car s) (car (car rest))))
                (cons (cons (car s) nil) rest)
                (cons (cons (car s) (car rest)) (cdr rest))
            )
        )
    )
)

(expect (nondecreaselist '(1 2 3 1 2 3)) ((1 2 3) (1 2 3)))

(expect (nondecreaselist '(1 2 3 4 1 2 3 4 1 1 1 2 1 1 0 4 3 2 1))
        ((1 2 3 4) (1 2 3 4) (1 1 1 2) (1 1) (0 4) (3) (2) (1)))




;;;;;;;;;;;;;;;;;;;; Q3 ;;;;;;;;;;;;;;;;;
; ! Difficulty **
(define (directions n sym)
  (define (search s exp)
    ; Search an expression s for n and return an expression based on exp.
    (cond 
      ((number? s)
       (if (= s n) exp nil) )
      ((null? s)
       nil)
      (else
       (search-list s exp))))
  (define (search-list s exp)
    ; Search a nested list s for n and return an expression based on exp.
    (let ((first
           (search (car s) (cons 'car (cons exp nil))))
          (rest
           (search (cdr s) (cons 'cdr (cons exp nil)))))
      (if (null? first)
          rest
          first)))
  (search (eval sym) sym))

(define a '(1 (2 3) ((4))))

(expect (directions 1 'a) (car a))

(expect (directions 2 'a) (car (car (cdr a))))

(expect (directions 4 'a)  (car (car (car (cdr (cdr a))))))

(define b '((3 4) 5))

(expect (directions 4 'b) (car (cdr (car b))))
