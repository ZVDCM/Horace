# tested on Windows 10 Home and python 3.6 [at Great Istanbul, Turkey]
import subprocess
from time import perf_counter


class FindMinMtu:
    """
        - Find Minimum "Maximum Transmission Unit" of a packet routing path via Binary Search

        - Suppose you want to find how much data you can send in each packet
          from London to Turkey?
        - Now we need to remember MTU and MSS (Max. Segment size) isn't not the same.
          MSS is the actual data (not headers) you can send. A typical formula for MSS is
          MSS = MTU - (IP header_size  + TCP/UDP/Any Transport Layer Protocol header_size)
          whereas MTU = Everything in packet - Ethernet headers
          MTU typical refers to Ethernet MTU, AKA how much payload can an ethernet cable push through next hop.
    """

    def __init__(self, url: str):
        self.url = url

        self._low_mtu = 500
        # typically ethernet cables can carry 1500 bytes (but Jumbo fiber can carry upto 9K bytes AFAIK)
        # so increase it as per your requirements
        self._high_mtu = 1500
        self._last_accepted = self._low_mtu

    @staticmethod
    def yield_console_output(command):
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        return iter(p.stdout.readline, b'')

    def does_accept_mtu_size(self, size) -> bool:
        command = 'ping {domain_name} -t -f -l {size}'.format(domain_name=self.url,
                                                           size=size).split()
        for line in self.yield_console_output(command):
            line = line.decode(encoding='utf-8')
            if line.startswith('Packet') and 'DF' in line:
                return False
            elif line.startswith('Reply'):
                return True

    def find_min_mtu(self):
        while self._low_mtu <= self._high_mtu:
            if not (self.does_accept_mtu_size(self._low_mtu), self.does_accept_mtu_size(self._high_mtu)):
                return self._last_accepted
            else:
                middle = (self._high_mtu + self._low_mtu) // 2
                print("Low: {} High: {} Middle: {}".format(self._low_mtu, self._high_mtu, middle))
                if self.does_accept_mtu_size(middle):
                    self._last_accepted = middle
                    self._low_mtu = middle + 1
                else:
                    self._high_mtu = middle - 1
        return self._last_accepted


if __name__ == '__main__':
    start = perf_counter()
    # please provide protocol less domain name (without http://, https:// and also without www or any subdomain)
    # provide the naked url (without www/subdomain)
    f = FindMinMtu("libwired.com")
    print("\nMTU: {} bytes (Found in {} seconds)".format(f.find_min_mtu(), perf_counter() - start))