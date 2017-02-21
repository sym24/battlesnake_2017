function [ G ] = generateMoveset( currentFrame,weights,n,legend)
%GENERATEMOVESET Summary of this function goes here
%   Detailed explanation goes here


[r,c] = size(currentFrame);                        %# Get the matrix size
diagVec1 = repmat([ones(c-1,1); 0],r,1);  %# Make the first diagonal vector
                                          %#   (for horizontal connections)
diagVec1 = diagVec1(1:end-1);             %# Remove the last value
diagVec2 = ones(c*(r-1),1);               %# Make the second diagonal vector
                                          %#   (for vertical connections)
adj = diag(diagVec1,1)+...                %# Add the diagonals to a zero matrix
      diag(diagVec2,c);
%adj = adj+adj.';                         %'# Add the matrix to a transposed
                                          %#   copy of itself to make it
                                          %#   symmetric
% adj will be (n+2)x(n+2) but upper symetric
size(adj)
adj = adj*(weights(:)*weights(:)')


G = graph(adj,'upper');
plot(G,'EdgeLabel',G.Edges.Weight)

end