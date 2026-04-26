function [sol,err] = function_solve_lsoe(A , B)
%Gaussian elimination solution of matrix

err = 0;
    n = size(A,1);
    sol = zeros(n,1);

    if n~=size(B,1) || n~= size(A,2)
        error('Matrix dimensions must agree: A is %dx%d, b is %dx1', n, size(A,2), size(B,1))
    end

    for ix= 1:n-1
        %normalize
        maxRowFactor = max(abs(A(ix:end,ix:end)'))'
        A(ix:end,ix:end) =A(ix:end,ix:end)./maxRowFactor;
        B(ix:end) = B(ix:end) ./ maxRowFactor;

        %swap rows
        [~, pivotRow] = max(abs(A(ix:end,ix)));
        pivotRow = pivotRow + ix -1 ;
        if pivotRow ~= ix
            IP = eye(n);
            lIx = IP(ix,:);
            lPv = IP(pivotRow,:);

            IP(ix,:) = lPv;
            IP(pivotRow,:) = lIx;
            A = IP*A;
            B= IP*B;
        end

        %reduce
        M = eye(n);
        M(ix+1:end,ix) = -A(ix+1:end,ix)/A(ix,ix);
        A = M*A;
        B = M*B;
  
    end

    %back sub
    for ix = n:-1:1
        sol(ix) = (B(ix)-A(ix,ix+1:n)*sol(ix+1:n))/A(ix,ix);
    end

end

