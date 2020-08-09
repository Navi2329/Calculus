print("Hello world")

class ConstExpr:
    def _init_(self, const):
        self._const = const
    def differentiate(self):
        return ConstExpr(0)
    def pretty(self):
        return str(self._const)
        
class AddExpr:
    def _init_(self, lhs_expr, rhs_expr):
        self._lhs_expr = lhs_expr
        self._rhs_expr = rhs_expr
    def differentiate(self):
        return AddExpr(
            self._lhs_expr.differentiate(),
            self._rhs_expr.differentiate()
        )
    def pretty(self):
        return '(' + self._lhs_expr.pretty() + ') + (' +  self._rhs_expr.pretty() + ')'

class MulExpr:
    def _init_(self, lhs_expr, rhs_expr):
        self._lhs_expr = lhs_expr
        self._rhs_expr = rhs_expr
    def differentiate(self):
        return AddExpr(
            MulExpr(self._lhs_expr.differentiate(), self._rhs_expr),
            MulExpr(self._rhs_expr.differentiate(), self._lhs_expr)
        )
    def pretty(self):
        return '(' + self._lhs_expr.pretty() + ') * (' +  self._rhs_expr.pretty() + ')'

class PowerExpr:
    def _init_(self, power):
        self._power = power
        
    def differentiate(self):
        return MulExpr(ConstExpr(self._power), PowerExpr(self._power-1))
        
    def pretty(self):
        return 'x^' + str(self._power) 
        

a = PowerExpr(5)
print(a.differentiate().pretty())
