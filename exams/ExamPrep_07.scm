;;;;;;;;;;;;;;;;;;;; Q1 ;;;;;;;;;;;;;;;;;
; ! Difficulty **
(define (get-slicer a b)
  (define (slicer lst)
    (define (slicer-helper c i j)
      (cond 
        ((or (>= i j) (equal? c nil)) nil)
        ((= i 0) (cons (car c) (slicer-helper (cdr c) i (- j 1))))
        (else (slicer-helper (cdr c) (- i 1) (- j 1)))))
    (slicer-helper lst a b))
  slicer)

; DOCTESTS (No need to modify)
(define a '(0 1 2 3 4 5 6))
(define one-two-three (get-slicer 1 4))
(define one-end (get-slicer 1 10))
(define zero (get-slicer 0 1))
(define empty (get-slicer 4 4))

(expect (one-two-three a) (1 2 3))
(expect (one-end a) (1 2 3 4 5 6))
(expect (zero a) (0))
(expect (empty a) ())



;;;;;;;;;;;;;;;;;;;; Q2 ;;;;;;;;;;;;;;;;;
; ! Difficulty **
; helper function
(define (combine lst1 lst2 x)
  (if (equal? lst1 nil)
    lst2
    (cons (cons x (car lst1)) (combine (cdr lst1) lst2 x))))

(expect (combine '((1)) '((3) (4 5)) 0) ((0 1) (3) (4 5)))
(expect (combine '((1) (2 3) (3)) '((4 5) (6)) 'a) ((a 1) (a 2 3) (a 3) (4 5) (6)))

(define (partition-options total biggest)
  (cond
    ((= total 0) (cons nil nil))
    ((or (= biggest 0) (< total 0)) nil)
    (else (let 
      ((w (partition-options (- total biggest) biggest))
      (wo (partition-options total (- biggest 1))))
      (combine w wo biggest)))))

(expect (partition-options 2 2) ((2) (1 1)))
(expect (partition-options 3 3) ((3) (2 1) (1 1 1)))
(expect (partition-options 4 3) ((3 1) (2 2) (2 1 1) (1 1 1 1)))




;;;;;;;;;;;;;;;;;;;; Q3 ;;;;;;;;;;;;;;;;;
; ! Difficulty **
(define (tree label branches) (cons label branches))
(define (label t) (car t))
(define (branches t) (cdr t))
(define (is-leaf t) (null? (branches t)))

(define (find-in-tree t goal)
  (if (equal? (label t) goal)
    (cons goal nil)
    (let ((path (find-in-branches (branches t) goal)))
      (if (equal? path nil)
        nil
        (cons (label t) path)))))

(define (find-in-branches bs goal)
  (if (equal? bs nil)
    nil
    (let ((path (find-in-tree (car bs) goal)))
      (if (equal? path nil)
        (find-in-branches (cdr bs) goal)
        path))))

; DOCTESTS (no need to modify)
(define t1 (tree 1
  (list
    (tree 2
      (list
        (tree 5 nil)
          (tree 6 (list
            (tree 8 nil)))))
    (tree 3 nil)
    (tree 4
      (list
        (tree 7 nil))))))

(expect (find-in-tree t1 7) (1 4 7))
(expect (find-in-tree t1 1) (1))
(expect (find-in-tree t1 12) ())
