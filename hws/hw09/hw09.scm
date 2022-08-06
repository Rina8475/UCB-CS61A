(define-macro (switch expr cases)
  (cons 'cond
        (map (lambda (case)
                        (cons `(equal? ,expr ',(car case)) (cdr case)))
             cases)))


; (define-macro (switch expr cases)
;   (cons _________
;         (map (_________ (_________)
;                         (cons _________ (cdr case)))
;              cases)))