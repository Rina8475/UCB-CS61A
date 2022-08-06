;;;;;;;;;;;;;;;;;;;; Q1 ;;;;;;;;;;;;;;;;;
; ! Difficulty *
(define (repeater expr k)
  ; Returns a list with k copies of expr
  (if (= k 0)
      nil
      (cons expr (repeater expr (- k 1)))))

(expect (repeater 2 0) ())
(expect (repeater 2 5) (2 2 2 2 2))

(define-macro (arg-repeater fn expr k)
  ; Fills in fn with k copies of expr
  (cons fn (repeater expr k)))

(define (add-four a b c d) (+ a b c d))
(define (mult-one x) x)
(define (mult-seven a1 a2 a3 a4 a5 a6 a7)
  (* a1 a2 a3 a4 a5 a6 a7))

(expect (arg-repeater add-four 10 4) 40)
(expect (arg-repeater mult-one -2 1) -2)
; 2 multiplied to itself 7 times = 2^7 = 128
(expect (arg-repeater mult-seven 2 7) 128)




;;;;;;;;;;;;;;;;;;;; Q2 ;;;;;;;;;;;;;;;;;
; ! Difficulty **
(define (replace-helper e o n)
  (cond ((equal? e nil) nil)
        ((list? (car e)) (cons (replace-helper (car e) o n) (replace-helper (cdr e) o n)))
        ((equal? (car e) o) (cons n (replace-helper (cdr e) o n)))
        (#t (cons (car e) (replace-helper (cdr e) o n)))
  )
)
(define-macro (replace expr old new)
    (replace-helper expr old new))

(replace (define (repeat-nested x n) (if (= n 0) nil (cons x (repeat-nested x (- n 1))))) cons list)
(replace (define x 3) 3 5)

(define nested (replace (cons 1 (cons 2 (cons 3 (cons 4 nil)))) cons list))

(expect x 5)
(expect nested (1 (2 (3 (4 ())))))
(expect (repeat-nested 5 3) (5 (5 (5 ()))))




;;;;;;;;;;;;;;;;;;;; Q3 ;;;;;;;;;;;;;;;;;
; ! Difficulty *
(define (remove lst idxs)
  ; return items of list that aren't at idxs
  (cond 
    ((equal? idxs nil) lst)
    ((= (car idxs) 0) (remove (cdr lst) (map (lambda (x) (- x 1)) (cdr idxs))))
    (else
     (cons (car lst) (remove (cdr lst) (map (lambda (x) (- x 1)) idxs))))))

(expect (remove '(10 9 8 7 6 5 4) '(0 2 3)) (9 6 5 4))
(expect (remove '(10 9 8 7 6 5 4) '()) (10 9 8 7 6 5 4))

; Q3

(define (splice args indices vals)
  (cond 
    ((equal? indices nil) args)
    ((= (car indices) 0)
     (cons (car vals) (splice (cdr args) 
                              (map (lambda (x) (- x 1)) (cdr indices))
                              (cdr vals))))
    (else
     (cons (car args) (splice (cdr args)
                              (map (lambda (x) (- x 1)) indices)
                              vals)))))

(expect (splice '(10 9 8 7 6 5 4) '(0 2 3) '(a b c)) (a 9 b c 6 5 4))

(define-macro (k-curry fn args vals indices)
  (let ((args-left (remove args indices))
        (spliced-args (splice args indices vals)))
    `(lambda ,args-left (,fn ,@spliced-args))))

(define (f a b c d) (- (+ a c) (+ b d)))
(define minus-six (k-curry f (a b c d) (2 4) (1 3)))

; (10 + 8) - 6
(expect (minus-six 8 10) 12)
