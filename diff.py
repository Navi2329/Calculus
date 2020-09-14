from fractions import Fraction
from sympy import *
from sympy.abc import x,y
def match_for_binary_exp(expr, klass, op):
    atom_expr = None
    expr_length = 0
    if len(expr) < 3:
        return None
    for i in range(len(expr), 1, -1):
        atom_expr = AtomicExpr.match(expr[0:i])
        if atom_expr is not None:
            expr_length = i
            break

    if atom_expr is None:
        return None
    if expr[expr_length] != op:
        return None
    second_atom_expr = AtomicExpr.match(expr[expr_length+1:])
    if second_atom_expr is None:
        return None
    return klass(atom_expr, second_atom_expr)
  
  
   
class Expr:
    def __init__(self):

        pass

    def differentiate(self):

        return None

    def is_zero(self):

        return isinstance(self, ConstExpr) and self._const == 0
      
    @staticmethod
    def match(expr):
        classes = [
            AddExpr,
            SubtractExpr,
            MulExpr,
            DivExpr,
            log,
            sin,
            cos,
            tan,
            cot,
            cosec,
            sec,
          	arcsin,
          	arccos,
          	arctan,
            arccot,
            arcsec,
            arccosec,
            power1,
            AtomicExpr,
          	PowerExpr,
          	ConstExpr,
        ]
        for klass in classes:
            exp = klass.match(expr)
            if exp is not None:
                return exp
        return None

class AtomicExpr(Expr):
    @staticmethod
    def match(expr):
        if len(expr) < 3:
            return None
        if expr[0] == '(' and expr [len(expr)-1] == ')':
            exp = (Expr.match(expr[1:len(expr)-1]))
            return exp
        return None


class ConstExpr(Expr):

    def __init__(self, const):

        self._const = const

    def differentiate(self):

        return ConstExpr(0)

    def pretty(self):

        return '('+str(self._const)+')'
      
    @staticmethod
    def match(expr):
      try:
        value = int(expr)
      except:
        return None
      return ConstExpr(value)

    def simplify(self):

        return self

       

class AddExpr(Expr):

    def __init__(self, lhs_expr, rhs_expr):

        self._lhs_expr = lhs_expr

        self._rhs_expr = rhs_expr

    def differentiate(self):

        return AddExpr(

            self._lhs_expr.differentiate(),

            self._rhs_expr.differentiate()

        )


    def simplify(self):

        self._lhs_expr = self._lhs_expr.simplify()

        self._rhs_expr = self._rhs_expr.simplify()

        if self._lhs_expr.is_zero():

            return self._rhs_expr

        if self._rhs_expr.is_zero():

            return self._lhs_expr

        return self
      
    @staticmethod
    def match(expr):
        return match_for_binary_exp(expr, AddExpr, '+')

    def pretty(self):

        return '(' + self._lhs_expr.pretty() + ') + (' +  self._rhs_expr.pretty() + ')'

class SubtractExpr(Expr):

    def __init__(self, lhs_expr, rhs_expr):

        self._lhs_expr = lhs_expr

        self._rhs_expr = rhs_expr

    def differentiate(self):

        return SubtractExpr(

            self._lhs_expr.differentiate(),


            self._rhs_expr.differentiate()

        )
    def simplify(self):

        self._lhs_expr = self._lhs_expr.simplify()

        self._rhs_expr = self._rhs_expr.simplify()

        if self._lhs_expr.is_zero():

            return self._rhs_expr

        if self._rhs_expr.is_zero():

            return self._lhs_expr

        return self
      
    @staticmethod
    def match(expr):
        return match_for_binary_exp(expr, SubtractExpr, '-')


    def simplify(self):

        self._lhs_expr = self._lhs_expr.simplify()

        self._rhs_expr = self._rhs_expr.simplify()

        if self._lhs_expr.is_zero():

            return self._rhs_expr

        if self._rhs_expr.is_zero():

            return self._lhs_expr

        return self

    def pretty(self):

        return '(' + self._lhs_expr.pretty() + ') - (' +  self._rhs_expr.pretty() + ')'


class MulExpr(Expr):

    def __init__(self, lhs_expr, rhs_expr):

        self._lhs_expr = lhs_expr

        self._rhs_expr = rhs_expr

    def differentiate(self):

        return AddExpr(

            MulExpr(self._lhs_expr.differentiate(), self._rhs_expr),

            MulExpr(self._rhs_expr.differentiate(), self._lhs_expr)

        )
    
    @staticmethod
    def match(expr):
        return match_for_binary_exp(expr, MulExpr, '*')

    def simplify(self):

        self._lhs_expr = self._lhs_expr.simplify()

        self._rhs_expr = self._rhs_expr.simplify()

        if self._lhs_expr.is_zero():

            return ConstExpr(0)

        if self._rhs_expr.is_zero():

            return ConstExpr(0)

        return self

    def pretty(self):

        return '('+ self._lhs_expr.pretty() + ') * (' +  self._rhs_expr.pretty() + ')'
    
class DivExpr(Expr):
    def __init__(self,numExpr,denoExpr):
        self.numExpr=numExpr
        self.denoExpr=denoExpr
    def differentiate(self):
        return(
            DivExpr((SubtractExpr(MulExpr(self.denoExpr,self.numExpr.differentiate()),(MulExpr((self.numExpr),self.denoExpr.differentiate())))),MulExpr(self.denoExpr,self.denoExpr)))
    
    @staticmethod
    def match(expr):
        return match_for_binary_exp(expr, DivExpr, '/')
      
    def pretty(self):
        return '(' + self.numExpr.pretty() + ') / (' + self.denoExpr.pretty() + ')' 
class PowerExpr(Expr):

    def __init__(self, power):

        self._power = power

       

    def differentiate(self):

        return MulExpr(ConstExpr(self._power), PowerExpr(self._power-1))

    
    @staticmethod
    def match(expr):
        if len(expr) >= 3 and expr[0] == 'x' and expr[1] == '^':
          try:
            const = int(expr[2:])
            return PowerExpr(const)
          except:
             pass
        elif expr == 'x':
          return PowerExpr(1)

    def simplify(self):

        if self._power == 0:

            return ConstExpr(1)

        return self

    def pretty(self):
        return 'x^' + str(self._power)

class sqrt(Expr):
    def __init__(self,expr):
        self.expr=expr
    def  pretty(self):
        return '('+self.expr.pretty()+')**(1/2)'
    def simplify(self):
        return self

class power1(Expr):
    def __init__(self,expr,power):
        self.expr=expr
        self.power=power
    def differentiate(self):
        return MulExpr(power1(self.expr,self.power),AddExpr(MulExpr(self.power.differentiate(),log(self.expr)),MulExpr(DivExpr(self.expr.differentiate(),self.expr),self.power)))
    @staticmethod
    def match(expr):
        return match_for_binary_exp(expr, power1, '^')
    def pretty(self):
        return '('+self.expr.pretty()+')**('+self.power.pretty()+')'
    def simplify(self):
        pass


class comp(Expr):
    def __init__(self,outerExpr,innerExpr):
        self.innerExpr=innerExpr
        self.outerExpr=outerExpr
    def differentiate(self):
        return MulExpr(comp(self.outerExpr.differentiate(),self.idefnnerExpr),self.innerExpr.differentiate())
    def pretty(self):
        return "(" + self.outerExpr.pretty() + "(" + self.innerExpr.pretty() + "))"
    def simplify(self):
        return self

def match_unary(expr, klass, comp):
    if expr[0:len(comp)] != comp:
        return None
    exp = AtomicExpr.match(expr[len(comp):])
    if exp is None:
        return None
    return klass(exp)

  
class mod(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),DivExpr(self.expr,mod(self.expr)))
    def pretty(self):
        return 'Abs('+self.expr.pretty()+')'
    @staticmethod
    def match(expr):
        return match_unary(expr, mod, 'mod')

      
      
      
      
      
class log(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),DivExpr(MulExpr(ConstExpr(1),PowerExpr(0)),self.expr))
    def pretty(self):
        return 'log('+self.expr.pretty()+')'
    def simplify(self):
        return self
    @staticmethod
    def match(expr):
        return match_unary(expr, log, 'log')

class exp(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),exp(self.expr))
    def pretty(self):
        return 'e**('+self.expr.pretty()+')'

class sin(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),cos(self.expr))
    def pretty(self):
        return 'sin('+self.expr.pretty()+')'
    @staticmethod
    def match(expr):
        return match_unary(expr, sin, 'sin')

class cos(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),MulExpr(ConstExpr(-1),sin(self.expr)))
    def pretty(self):
        return "cos("+self.expr.pretty()+")"
    def simplify(self):
        return self
    @staticmethod
    def match(expr):
        return match_unary(expr, cos, 'cos')
      
class tan(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),MulExpr(sec(self.expr),sec(self.expr)))
    def pretty(self):
        return "tan("+self.expr.pretty()+")"
    @staticmethod
    def match(expr):
        return match_unary(expr, tan, 'tan')
    
class sec(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),MulExpr(sec(self.expr),tan(self.expr)))
    def pretty(self):
        return "sec("+self.expr.pretty()+")"
    def simplify(self):
        return self
    @staticmethod
    def match(expr):
        return match_unary(expr, sec, 'sec')

class cosec(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),MulExpr(ConstExpr(-1),MulExpr(cosec(self.expr),cot(self.expr))))
    def pretty(self):
        return "cosec("+self.expr.pretty()+")"
    @staticmethod
    def match(expr):
        return match_unary(expr, cosec, 'cosec')
        
class cot(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),MulExpr(ConstExpr(-1),MulExpr(cosec(self.expr),cosec(self.expr))))
    def pretty(self):
        return "cot("+self.expr.pretty()+")"
    def simplify(self):
        return self
    @staticmethod
    def match(expr):
        return match_unary(expr, cot, 'cot')

class arcsin(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),DivExpr(MulExpr(ConstExpr(1),PowerExpr(0)),sqrt(SubtractExpr(MulExpr(ConstExpr(1),PowerExpr(0)),MulExpr(self.expr,self.expr)))))
    def pretty(self):
        return 'arcsin('+self.expr.pretty()+')' 
    @staticmethod
    def match(expr):
        return match_unary(expr, arcsin, 'arcsin')

class arccos(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),DivExpr(MulExpr(ConstExpr(-1),PowerExpr(0)),sqrt(SubtractExpr(MulExpr(ConstExpr(1),PowerExpr(0)),MulExpr(self.expr,self.expr)))))
    def pretty(self):
        return 'arccos('+self.expr.pretty()+')'  
    @staticmethod
    def match(expr):
        return match_unary(expr, arccos, 'arccos')
class arctan(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),DivExpr(MulExpr(ConstExpr(1),PowerExpr(0)),AddExpr(MulExpr(ConstExpr(1),PowerExpr(0)),MulExpr(self.expr,self.expr))))
    def pretty(self):
        return 'arctan('+self.expr.pretty()+')'
    @staticmethod
    def match(expr):
        return match_unary(expr, arctan, 'arctan')
class arccot(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),DivExpr(MulExpr(ConstExpr(-1),PowerExpr(0)),AddExpr(MulExpr(ConstExpr(1),PowerExpr(0)),MulExpr(self.expr,self.expr))))
    def pretty(self):
        return 'arccot('+self.expr.pretty()+')'
    @staticmethod
    def match(expr):
        return match_unary(expr, arccot, 'arccot')
class arcsec(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),DivExpr(MulExpr(ConstExpr(1),PowerExpr(0)),MulExpr(mod(self.expr),sqrt(SubtractExpr(MulExpr(ConstExpr(1),PowerExpr(0)),MulExpr(self.expr,self.expr))))))
    def pretty(self):
        return 'arcsec('+self.expr.pretty()+')'
    @staticmethod
    def match(expr):
        return match_unary(expr, arcsec, 'arcsec')
class arccosec(Expr):
    def __init__(self,expr):
        self.expr=expr
    def differentiate(self):
        return MulExpr(self.expr.differentiate(),DivExpr(MulExpr(ConstExpr(-1),PowerExpr(0)),MulExpr(mod(self.expr),sqrt(SubtractExpr(MulExpr(ConstExpr(1),PowerExpr(0)),MulExpr(self.expr,self.expr))))))
    def pretty(self):
        return 'arccosec('+self.expr.pretty()+')'
    @staticmethod
    def match(expr):
        return match_unary(expr, arccosec, 'arccosec')


'''def diff(expr):
    a=sympify(differentiate(expr).pretty())
    print(sympify(differentiate(expr).pretty()))'''
    
    
def parse_and_differentiate(expr_string):
  input_expr = Expr.match(expr_string)
  global ex
  print(input_expr.pretty())
  ex=sympify(input_expr.pretty())
  print(sympify(ex))
  
  return input_expr.differentiate()

def input_handler():
    print('1)To find DERIVATIVE')
    print('2)To find DERIVATIVE AT A POINT')
    print('3)To find slope of tangent to the curve at a point')
    print('4)To find slope of normal to the curve at a point')
    print('5)To find equation of tangent at a point on curve')
    print('6)To find equation of normal at a point on curve')
    print('7)To enter another function')
    print('8)EXIT')
    print('YOU CAN ENTER THE FUNCTION')
    value = parse_and_differentiate(input())
    a=sympify(value.pretty())
    ans='yes'
    list=[2,3,4,5,6]
    while ans=='yes':
        c=int(input('Enter choice'))
        if c in list:
            q=input('Enter x')
            
            if c==2:
                b=str(a).replace('x','('+q+')')
                print('DERIVATIVE OF CURVE AT x='+q+' is',N(b))
            elif c==3:
                b=str(a).replace('x','('+q+')')
                print('SLOPE OF NORMAL TO CURVE AT x='+q+' is',-1/N(b))
            elif c==4:
                b=str(ex).replace('x','('+q+')')
                print('VALUE OF FUNCTION AT x='+q+' is',N(b))
            elif c==5:
                print('Equation of tangent at x='+q+' is')
                m=N(str(a).replace('x','('+q+')'))
                y=N(str(ex).replace('x','('+q+')'))
                c=N(y-(m*int(q)))
                m=Fraction(float(m))
                c=Fraction(float(c))
                if m==1:
                    if c==0:
                        eq='y=x'
                    elif c>0:
                        eq='y=x'+'+'+str(c)
                    else:
                        eq='y=x'+str(c)
                else:
                    if c==0:
                        eq='y='+str(m)+'x'
                    elif c>0:
                        eq='y='+str(m)+'x'+'+'+str(c)
                    else:
                        eq='y='+str(m)+'x'+str(c)
                print(eq)
            elif c==6:
                print('Equation of normal at x='+q+' is')
                m=N(str(a).replace('x','('+q+')'))
                m=Fraction(-1,Fraction(float(m)))
                y=N(str(ex).replace('x','('+q+')'))
                c=N(y-(m*int(q)))
                c=round(c,1)
                if m==1:
                    if c==0:
                        eq='y=x'
                    elif c>0:
                        eq='y=x'+'+'+str(c)
                    else:
                        eq='y=x'+str(c)
                else:
                    if c==0:
                        eq='y=('+str(m)+')x'
                    elif c>0:
                        eq='y=('+str(m)+')x'+'+'+str(c)
                    else:
                        eq='y=('+str(m)+')x'+str(c)
                print(eq)
        if c==1:
            print('DERIVATIVE OF CURVE IS',a)
        elif c==7:
            input_handler()
        elif c==8:
            break
           
                    
def differentiate(Expr):
    return Expr.differentiate()
input_handler()
