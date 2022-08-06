(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

; Some utility functions that you may find useful to implement

(define (zip pairs)
    (if (equal? pairs nil) (pair nil nil)
        (let (
                 (x (zip (cdr pairs)))
                 (y (car pairs))
             )
             (pair (cons (car y) (car x))
                   (cons (cadr y) (cadr x)))
        ))
)

(define (pair x y)
    (cons x (cons y nil))
)


;; Problem 5
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 5
    (define (enumerate-iter s index)
        (if (equal? s nil) nil
            (cons (pair index (car s)) (enumerate-iter (cdr s) (+ index 1)))))
    (enumerate-iter s 0)
)
  ; END PROBLEM 5

;; Problem 6

;; Merge two lists LIST1 and LIST2 according to COMP and return
;; the merged lists.
(define (merge comp list1 list2)
  ; BEGIN PROBLEM 6
    (cond ((equal? list1 nil) list2)
          ((equal? list2 nil) list1)
          ((comp (car list1) (car list2))
                 (cons (car list1) (merge comp (cdr list1) list2)))
          (else (cons (car list2) (merge comp list1 (cdr list2))))
    )
)
  ; END PROBLEM 6



;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

;; Problem 7
(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         ; BEGIN PROBLEM 7
         expr
         ; END PROBLEM 7
         )
        ((quoted? expr)
         ; BEGIN PROBLEM 7
         `(quoted ,(let-to-lambda (cadr expr)))
         ; END PROBLEM 7
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM 7
           `(,form ,params ,@(map let-to-lambda body))
           ; END PROBLEM 7
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM 7
           (define args (zip values))
           `((lambda ,(car args) ,@(map let-to-lambda body)) ,@(cadr args))
           ; END PROBLEM 7
           ))
        (else
         ; BEGIN PROBLEM 7
         ;  (pair (car expr) (map let-to-lambda (cdr expr)))
         `(,(car expr) ,@(map let-to-lambda (cdr expr)))
         ; END PROBLEM 7
         )))

