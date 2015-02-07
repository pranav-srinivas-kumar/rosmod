﻿namespace Sharpen
{
    public interface Checksum
    {
        long Value
        {
            get;
        }

        void Reset();

        void Update(byte[] buffer, int offset, int length);

        void Update(int byteValue);
    }
}
