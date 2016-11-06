"1.2"
(define (min x y z)
	(if (< x y)
		(if (< x z) x z)
		(if (< y z) y z)
	)	
)
(define (f x y z)
	(- (+ x y z) (min x y z) ))

"1.7"
(define (good-enough? guess x)
	(< (/ (abs (- (improve guess x) guess))  
	        guess)  
	    0.001) )
”其他不变“


"1.8"
(define (good-enough? guess x)
	(< (/ (abs (- (improve guess x) guess))  
	        guess)  
	    0.001) )
(define (improve guess x)
	(/ (+ (/x (* y y)) 
	        (* 2 y)) 
	    3))
(define (cubic-iter guess x)
             (if (good-enough? guess x)
                  guess
                  (cubic-iter (improve guess x) 
                              x)   ))
(define (cubic x)
             (cubic-iter 1.0 x))

"”1.31“"
"“递归过程”"
(define (producut term  a next b)
 	(if (>a b)
 	     1		
 	      (* (term a)  
 	          (producut term (next a)  next b)   )))

(define (factorial n) 
	(define (self x) x )
	(define (inc x) (+ x 1))
	(producut self 1 inc n)
)

(define (pi/4 n)
	(define (term x)
		(if even? 
		     (/ (+ x 2) (+ x 1) )
		     (/ (+ x 1) (+ x 2) )  )	
	)
	(define (next x) (+ x 1))
	(product term 1 next n)

)
"“迭代过程”"
(define (product term a next b)
	(define (iter a result)
		(if (>a b)
			result	
			(iter (next a)  (* (term a) result) )
		)

	)
	(iter a 1)

)

"“1.32”
“递归过程”"
(define (accumulate combiner null-value term a next b)
    (if (> a b)
        null-value
        (combiner (term a)
                  (accumulate combiner
                              null-value
                              term
                              (next a)
                              next
                              b))))

(define (sum term a next b)
    (accumulate + 
                0 
                term 
                a 
                next 
                b))

(define (product term a next b)
    (accumulate *
                1 
                term
                a
                next
                b))

"“迭代过程”"
(define (accumulate combiner null-value term a next b)
    (define (iter a result)
        (if (> a b)
            result
            (iter (next a)
                  (combiner result (term a)))))
    (iter a null-value))

"”1.33“
"
(define (filtered-accumulate combine null-value term a next b valid?)
    (if (> a b)
        null-value
        (let ((rest-terms (filtered-accumulate combine
                                               null-value
                                               term
                                               (next a)
                                               next
                                               b
                                               valid?)))
            (if (valid? a)
                (combine (term a) rest-terms)
                rest-terms)   )))
"”计算素数和“"
(define (primes-sum a b)
    (filtered-accumulate + 
                         0
                         (lambda (x) x)
                         a
                         (lambda (i) (+ i 1))
                         b
                         prime?))
(define (prime-n n)
	(define (valid? x) 
		(and (= 1GCD(x,n)) (< x x) )
	)
	(filtered-accumulate *
	               1
	               (lambda (x) x)
	               1
	               (lambda(i) (+ i 1))
	               n
	               valid?
	)

)

"”1.35“"
(define golden-ratio
    (fixed-point (lambda (x) 
                     (+ 1 (/ 1 x)))
                 1.0))

"”1.37“
”迭代模式“"
(define (cont-frac  n d k)
	(define (iter i result)
		(if (= i 1)
		     (/ (n 1) result)
		     (iter (- i 1) (+ (d (- i 1)) (/(n i) result))  )	
		)	
	)
	(iter k (d k) )
)

"”递归模式“"
(define (cont-frac n d k)
	
	(define (recur i)
		(if (= i (+ k 1))
		     0
		     (/(n i) (+ (d i) (recur (+i1)) ) )	)	
	)
	(recur 1)
)

"”1.46“"
(define (iterative-improve good-enough? improve)
	(lambda (guess)
		(let ((next (improve guess)))
			(if (good-enough? guess next)
				next
				((iterative-improve good-enough? improve) next)
				)
			
			)))
"”另一种定义方法“"
(define (iterative-improve close-enough? improve)
    (lambda (first-guess)
        (define (try guess)
            (let ((next (improve guess)))
                (if (close-enough? guess next)
                    next
                    (try next))))
        (try first-guess)))

"”重写sqrt函数“"
(define (sqrt x)
	(define dx 0.000001)
	(define (close-enough? v1 v2) 
		(< (abs (- v1 v2)) dx)
	)
  (define (improve guess)
		(average guess (/ x guess))
	)
	(define (average x y)
		(/ (+ x y) 2)
	)
	(define (abs x)
	  (if (> x 0)
			x
			(- 0 x)
		)	
	)
	((iterative-improve close-enough? improve) 1.0)
)

"2.2"
(define (make-point x y)
	(cons x y)
)
(define (x-point z)
	(car z)
)
(define (y-point z)
	(cdr z)
)

(define (make-segment a b)
	(cons a b)
)
(define (start-segment c)
	(car c)
)
(define (end-segment c)
	(cdr c)
)
(define (midpoint-segment line)
	(let ((s (start-segment line))
	        (e (end-segment line))
	       )
	       (make-point (/ (+ (x-point s) (x-point e)) 2)   (/ (+ (y-point s) (y-point e)) 2))
	)
)

"2.5"
(define (exp2 x y)
	(define (iter i product)
		(if (= i y)
		     product
		     (iter (+ i 1) (* product x))			
		)
	)
	(iter 0 1)
)
(define (cons2 x y)
	(*(exp 2 x) (exp 3 y))
)
"求余数"
(define (remainder a b)
	(define (iter result)
		(if (> 0 result) 
			(+ result b)
			(iter (- result b))	
		)
	)
	(iter a)
)
(define (car2 c)
	(define (iter-a i)
		(if  (> (remainder c (exp 2 i)) 0)
			(- i 1)
			(iter-a (+ i 1))
		)
	)
	(iter-a 0)
)
(define (cdr2 c)
	(define (iter-a i)
		(if  (> (remainder c (exp 3 i)) 0)
			(- i 1)
			(iter-a (+ i 1))
		)
	)
	(iter-a 0))


"''2.7''"
(define (upper-bound interval)
	(max     (car interval)
		(cdr interval)))

(define (upper-bound interval)
	(min     (car interval)
		(cdr interval)))

"2.8"
(define (sub-interval x y)
    (make-interval (- (lower-bound x) (upper-bound y))
                             (- (upper-bound x)  (lower-bound y))))

"2.9"
(define (width interval)
     (*0.5 
         (- (upper-bound interval)  
             (lower-bound interval))))

''2.10''
 (define (div-interval x y) 
   (if (>= 0 (* (lower-bound y) (upper-bound y))) 
       (error "Division error (interval spans 0)" y) 
       (mul-interval x  
                     (make-interval (/ 1. (upper-bound y)) 
                                    (/ 1. (lower-bound y)))))) 

 ''2.12''
  (define (make-interval-center-percent c pct) 
   (let ((width (* c (/ pct 100.0)))) 
     (make-interval (- c width) (+ c width)))) 
  
 (define (percent i) 
   (let ((center (/ (+ (upper-bound i) (lower-bound i)) 2.0)) 
         (width (/ (- (upper-bound i) (lower-bound i)) 2.0))) 
     (* (/ width center) 100))) 

"2.13"
(x,p1)*(y,p2)=>(xy,p1+p2)

"2.28"
(define (fringe items)
  (if (null? items)
	(list )
	 (if (pair? (car items))
	      (append (fringe (car items)) (fringe (cdr items)))
	      (cons (car items) (fringe (cdr items)))	
	 )
  )
)

"2.9"
(define (make-mobile left right)
   (list left right)
)
(define (make-branch len structure)
  (list len structure)
)
(define (left-branch mobile)
    (car mobile)
)
(define (right-branch mobile)
	(car (cdr mobile))
)
(define (brach-length branch)
  (car branch)
)
(define (branch-structure branch)
   (car (cdr branch))
)
(define (total-weight mobile)
	(if (not (pair? (branch-structure mobile)))
		(branch-structure mobile)
		(+ (total-weight (left-branch mobile)) (total-weight (right-branch mobile)) )	
))


"2.41"
(define (accumulate op initial sequence)
 (if (null? sequence)
      initial
      (op (car sequence)
             (accumulate op initial (cdr sequence)))
 )
)
(define (enumerate-interval low high)
  (if (> low high)
      (list )
      (cons low (enumerate-interval (+ low 1) high))
  )
)

(define (tri n s)
    (define (tri-tupple j k)
          (map (lambda (i)   (list i j k))  
          	(enumerate-interval 1 (- j 1))))

    (define (equal-s li )
    	(= s (accumulate + 0 li))
    )
    (define (iter1 k )
    	(define (iter-2 j)
    	     (if (< j 2)
    	          (list )
    	          (append (tri-tupple j k) (iter-2 (- j 1))))
    	)
             (iter-2 (- k 1))
    )
    (define (iter n)
         (if (< n 3)
             (list )
             (append (iter1 n)  (iter (- n 1) ))
         )
    )
    (filter less-s (iter n))

)

"2.54"
(define (equal? a b)
	(cond    ((and (null? a) (null? b)) #t)
		((or (null? a) (null? b))  #f)
		((and (not (pair? a))   (not (pair? b))  )   (eq? a b))
	             ((and (pair? a) (pair?b) (equal? (car a) (car b)))  (equal? (cdr a) (cdr b)))
	             (else #f)
	)
)


"2.61"
(define (adjoin-set x set)
	(if (null? set)
                  (list x)
                  (let  ((x1 (car set)))
                     (cond ((= x x1  set)

                             ((< x x1  (cons x set))
                             (else (cons ( x1 (adjoin-set x (cdr set)))))
                      ))

             )
	
)))
"2.62"
(define (union-set set another)
    (cond ((and (null? set) (null? another))
            '())
          ((null? set)
            another)
          ((null? another)
            set)
          (else
            (let ((x (car set)) (y (car another)))
                (cond ((= x y)
                        (cons x (union-set (cdr set) (cdr another))))
                      ((< x y)
                        (cons x (union-set (cdr set) another)))
                      ((> x y)
                        (cons y (union-set set (cdr another)))))))))

(define (install-derive-package)
	(define (derive-sum exp var)
		(make-sum (derive (addend exp) var)
			       (derive (augend exp)  var))
	)
	(define (derive-product exp var)
		(make-sum
			(make-product (mulyiplier exp)(derive (multiplicand exp) var))
			(make-product (derive (multiplier exp) var) (multiplicand exp))
		)
	)

	(put 'derive '+ derive-sum)
	(put 'derive '* derive-product)

)

"2.79"
(define (equ? x y)
    (apply-generic 'equ? x y))
"然后分别在几个包中实现这个 equ? 函数的数据导向操作。"

"3.1"
(define (make-accumulator init)
  (lambda (x)  (begin (set! init (+ init x))  init) )
)
"3.2"
(define (make-monitored f)
  (begin (set! count 0)
    (lambda (op)

      (cond ((eq? op 'how-many-calls) count)
        ((eq? op 'reset-count) (begin (set! count 0) count))
        (else (begin (set! count (+ count 1)) (f op))) 
      )
    )
  )
)
"3,6"

(define rand
	(let ((init 1))
		(lambda (parameter) 
		  (cond ((eq? parameter 'generate) (begin (set! init (rand-update init)) init))
		  	  ((eq? parameter 'reset) (lambda (new-value) (set! init new-value))) 
		  	  (else (error 'unkown_input)))

		)
	) 
	
)
















