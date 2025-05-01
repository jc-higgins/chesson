# ♟️ Chess Engine (Python → Rust/C++)

A custom-built chess engine written in Python with plans to migrate core components to Rust or C++ for performance. The project is designed to be modular, easy to understand, and incrementally optimized as it evolves.

---

## 🚀 Goals

- ✅ Build a fully functional chess engine in Python  
- 🧠 Learn and implement core chess engine principles (move generation, search, evaluation)  
- 🔁 Support move making/unmaking and game state tracking  
- 🧮 Integrate a basic evaluation function and search algorithm  
- ⚡ Later: Port performance-critical parts (move generation, search) to Rust or C++  
- ♜ Optional: Implement UCI protocol to connect to chess GUIs (e.g., Lichess, Arena)  

---

## 📐 Architecture Overview

chess_engine
├── board.py         # Board representation and FEN parsing
├── movegen.py       # Move generation (pseudo-legal and legal)
├── search.py        # Minimax and alpha-beta pruning
├── eval.py          # Static evaluation function
├── main.py          # Engine loop or CLI interface
├── uci.py           # (Optional) UCI Protocol support
└── tests/           # Unit tests for all modules


---

## 📆 Project Roadmap

### Phase 1: Core Engine in Python
- [ ] Board representation and print functionality
- [ ] Basic move generation (start with pawns and knights)
- [ ] Make/Unmake move handling
- [ ] Simple evaluation function (material count)
- [ ] Basic Minimax search
- [ ] Add Alpha-Beta pruning

### Phase 2: Expansion
- [ ] Full legal move generation (check validation)
- [ ] Support castling, en passant, and promotion
- [ ] Zobrist hashing and transposition tables
- [ ] Iterative deepening & quiescence search
- [ ] Time controls

### Phase 3: Optimization
- [ ] Profile slow functions
- [ ] Rewrite performance-critical sections in Rust or C++
- [ ] Bind with Python via `PyO3`, `cffi`, or `ctypes`

### Phase 4: Optional Features
- [ ] UCI protocol support
- [ ] Opening book integration
- [ ] Endgame tablebase support
- [ ] GUI or Web interface

---

## 🧠 References & Learning

- [Computer Chess Wiki](https://www.chessprogramming.org/Main_Page)  
- [UCI Protocol Spec](https://gist.github.com/bagaturchess/09a346e54e34c8c36ef4)  
- [PyChess Engine](https://github.com/pychess/pychess)  

---

## 🛠 Setup & Run

```bash
git clone https://github.com/yourname/chess-engine.git
cd chess-engine
python main.py
