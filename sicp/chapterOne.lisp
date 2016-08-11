“1.2”
(define (min x y z)
	(if (< x y)
		(if (< x z) x z)
		(if (< y z) y z)
	)	
)
(define (f x y z)
	(- (+ x y z) (min x y z) ))

“1.7”
(define (good-enough? guess x)
	(< (/ (abs (- (improve guess x) guess))  
	        guess)  
	    0.001) )
”其他不变“


“1.8”
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

”1.31“
“递归过程”
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
“迭代过程”
(define (product term a next b)
	(define (iter a result)
		(if (>a b)
			result	
			(iter (next a)  (* (term a) result) )
		)

	)
	(iter a 1)

)

“1.32”
“递归过程”
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

“迭代过程”
(define (accumulate combiner null-value term a next b)
    (define (iter a result)
        (if (> a b)
            result
            (iter (next a)
                  (combiner result (term a)))))
    (iter a null-value))

”1.33“

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
”计算素数和“
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

”1.35“
(define golden-ratio
    (fixed-point (lambda (x) 
                     (+ 1 (/ 1 x)))
                 1.0))

”1.37“
”迭代模式“
(define (cont-frac  n d k)
	(define (iter i result)
		(if (= i 1)
		     (/ (n 1) result)
		     (iter (- i 1) (+ (d (- i 1)) (/(n i) result))  )	
		)	
	)
	(iter k (d k) )
)
”递归模式“
(define (cont-frac n d k)
	
	(define (recur i)
		(if (= i (+ k 1))
		     0
		     (/(n i) (+ (d i) (recur (+i1)) ) )	)	
	)
	(recur 1)
)

”1.46“
(define (iterative-improve good-enough? improve)
	(lambda (guess)
		(let ((next (improve guess)))
			(if (good-enough? guess next)
				next
				((iterative-improve good-enough? improve) next)
				)
			
			)))
”另一种定义方法“
(define (iterative-improve close-enough? improve)
    (lambda (first-guess)
        (define (try guess)
            (let ((next (improve guess)))
                (if (close-enough? guess next)
                    next
                    (try next))))
        (try first-guess)))

”重写sqrt函数“
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
(define (exp x y)
	(define (iter i product)
		(if (= i y)
		     product
		     (iter (+ i 1) (* product x))			
		)
	)
	(iter 0 1)
)
(define (cons x y)
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
(define (car c)
	(define (iter-a i)
		(if  (> (remainder c (exp 2 i)) 0)
			(- i 1)
			(iter-a (+ i 1))
		)
	)
	(iter-a 0)
)
(define (cdr c)
	(define (iter-a i)
		(if  (> (remainder c (exp 3 i)) 0)
			(- i 1)
			(iter-a (+ i 1))
		)
	)
	(iter-a 0)
)