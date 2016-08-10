//1.2
(define (min x y z)
	(if (< x y)
		(if (< x z) x z)
		(if (< y z) y z)
	)	
)
(define (f x y z)
	(- (+ x y z) (min x y z) ))

//1.7
(define (good-enough? guess x)
	(< (/ (abs (- (improve guess x) guess))  
	        guess)  
	    0.001) )
其他不变


//1.8
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

//1.31
//递归过程
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
//迭代过程
(define (product term a next b)
	(define (iter a result)
		(if (>a b)
			result	
			(iter (next a)  (* (term a) result) )
		)

	)
	(iter a 1)

)

//1.32
//递归过程
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

//迭代过程
(define (accumulate combiner null-value term a next b)
    (define (iter a result)
        (if (> a b)
            result
            (iter (next a)
                  (combiner result (term a)))))
    (iter a null-value))

//1.33

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
//计算素数和
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

//1.35
(define golden-ratio
    (fixed-point (lambda (x) 
                     (+ 1 (/ 1 x)))
                 1.0))