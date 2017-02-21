function [ output_args ] = generateWalls( n )
%GENERATEWALLS create an empty array with walls around the outside
%   creates an (n+2)x(n+2) array where the walls around the outside are ones

output_args = zeros(n+2);
output_args(1,:) = ones(1,n+2);
output_args(n+2,:) = ones(1,n+2);
output_args(:,1) = ones(n+2,1);
output_args(:,n+2) = ones(n+2,1);

end