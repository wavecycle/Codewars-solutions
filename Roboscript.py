import re, numpy as np, time

class GridSolver(object):
	def __init__(self):
		pass
		
	def code_to_grid(self, code):
		self.code = code
		self.grid, self.facing_mod = np.array([[1]]), np.array([[-1, 0], [0, 1], [1, 0], [0, -1]])
		self.funcs = dict()
		self.parse_funcs()
		self.expand_rep()
		self.grid_navigate()
		return self.grid_printable()
		
	def parse_funcs(self, patt=r'(p(\d*)\(?([FLR\d]*)\)?(\d*)q)'):
		self.code_parsed = re.sub(patt, lambda x: self.funcs.setdefault(x[2], x[3] * int(x[4] or '1')) and '', self.code)
		for fid, fcode in self.funcs.items():
			self.code_parsed = re.sub(fr'(P{fid})', fcode, self.code_parsed)	

	def expand_rep(self, patt=r'(\([FLR\d]*\))(\d*)'):
		while re.findall(patt, self.code):
			self.code = re.sub(patt, lambda x: x.group(1)[1:-1] * int(x.group(2) or '1'), self.code)

	def grid_expand(self, shape, facing):
		if facing in (0, 3): self.grid = np.insert(self.grid, 0, 0, facing==3)
		if facing == 1: self.grid = np.concatenate((self.grid, [[0] for x in range(shape[0])]), axis= 1)
		else: self.grid = np.concatenate((self.grid, [[0 for x in range(shape[1])]]), axis=0)

	def grid_printable(self):
		return '\r\n'.join([''.join([x for x in row]) for row in self.grid])

	def grid_navigate(self, facing=1):
		pos, path_points = np.array([0, 0]), np.array([[ 0, 0]])
		for com, rep in re.findall(r'([FLR])(\d*)', self.code):
			for _ in range(int(rep or '1')):
				if com in 'LR':
					facing = (facing - 1)%4 if com[0] == 'L' else (facing + 1)%4
				else:
					pos += self.facing_mod[facing]
					path_points = np.concatenate(([pos], path_points), axis=0)
		new = np.unique(path_points, axis=0)
		(rm, cm), (rM, cM) = np.min(new, axis=0), np.max(new, axis=0)
		newlist = new.tolist()
		self.grid = [['*' if [row, col] in newlist else ' ' for col in range(cm, cM+1)]  for row in range(rm, rM+1)]


def execute(code):
	return t.code_to_grid(code)

t = GridSolver()
