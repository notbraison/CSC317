// Stack class
class Stack {

	// Array is used to implement stack
	constructor()
	{
		this.items = [];
	}

	// Functions to be implemented
	// push(item)
    push(element){
        this.items.push(element);
    }
	// pop()
    pop(){
         // return top most element in the stack
    // and removes it from the stack
    // Underflow if stack is empty
        if(this.items.length===0){
            return "underflow";
            return this.items.pop();
        }
    }
	// peek()
    // return the top most element from the stack but does'nt delete it.
    peek(){ 
       return this.items[this.items.length - 1] ;
    }
    
	// isEmpty()
    isEmpty()
{
    // return true if stack is empty
    return this.items.length == 0;
}
	// printStack()
    printStack()
{
    var str = "";
    for (var i = 0; i < this.items.length; i++)
        str += this.items[i] + " ";
    return str;
}
}

class Queue {
    constructor() {
        this.items = {}
        this.frontIndex = 0
        this.backIndex = 0
    }
    enqueue(item) {
        this.items[this.backIndex] = item
        this.backIndex++
        return item + ' inserted'
    }
    dequeue() {
        const item = this.items[this.frontIndex]
        delete this.items[this.frontIndex]
        this.frontIndex++
        return item
    }
    peek() {
        return this.items[this.frontIndex]
    }
    get printQueue() {
        return this.items;
    }
}

class WeightedGraph {//to create a weighted graph
    constructor() {
      this.adjacencyList = {};
    }
  
    addVertex(vertex) {
      if (!this.adjacencyList[vertex]) {
        this.adjacencyList[vertex] = [];
      }
    }
  
    addEdge(vertex1, vertex2, weight) {
      if (!this.adjacencyList[vertex1] || !this.adjacencyList[vertex2]) {
        return "Invalid vertex";
      }
  
      this.adjacencyList[vertex1].push({ node: vertex2, weight });
      this.adjacencyList[vertex2].push({ node: vertex1, weight });
    }
  
    // Example method: Display the graph
    displayGraph() {
      const vertices = Object.keys(this.adjacencyList);
      for (const vertex of vertices) {
        const connections = this.adjacencyList[vertex].map(
          ({ node, weight }) => `${node}(${weight})`
        );
        console.log(`${vertex} --> ${connections.join(", ")}`);
      }
    }
  }
  
  const romaniaGraph = new WeightedGraph();

// Adding cities as vertices
const cities = ["Arad", "Zerind", "Oradea", "Sibiu", "Timisoara", "Lugoj", "Mehadia", "Drobeta", "Craiova", "Rimnicu Vilcea", "Fagaras", "Pitesti", "Bucharest", "Giurgiu", "Urziceni", "Hirsova", "Eforie", "Vaslui", "Iasi", "Neamt"];
cities.forEach(city => romaniaGraph.addVertex(city));

romaniaGraph.addEdge("Arad", "Zerind", 75);
romaniaGraph.addEdge("Arad", "Timisoara", 118);
romaniaGraph.addEdge("Zerind", "Oradea", 71);
romaniaGraph.addEdge("Oradea", "Sibiu", 151);
romaniaGraph.addEdge("Timisoara", "Lugoj", 111);
romaniaGraph.addEdge("Lugoj", "Mehadia", 70);
romaniaGraph.addEdge("Mehadia", "Drobeta", 75);
romaniaGraph.addEdge("Drobeta", "Craiova", 120);
romaniaGraph.addEdge("Craiova", "Rimnicu Vilcea", 146);
romaniaGraph.addEdge("Rimnicu Vilcea", "Sibiu", 80);
romaniaGraph.addEdge("Rimnicu Vilcea", "Pitesti", 97);
romaniaGraph.addEdge("Sibiu", "Fagaras", 99);
romaniaGraph.addEdge("Pitesti", "Bucharest", 101);
romaniaGraph.addEdge("Bucharest", "Giurgiu", 90);
romaniaGraph.addEdge("Bucharest", "Urziceni", 85);
romaniaGraph.addEdge("Urziceni", "Hirsova", 98);
romaniaGraph.addEdge("Hirsova", "Eforie", 86);
romaniaGraph.addEdge("Urziceni", "Vaslui", 142);
romaniaGraph.addEdge("Vaslui", "Iasi", 92);
romaniaGraph.addEdge("Iasi", "Neamt", 87);

// Display the Romanian cities graph
romaniaGraph.displayGraph();

function dijkstras(graph,source){

    source=0;
    
}


