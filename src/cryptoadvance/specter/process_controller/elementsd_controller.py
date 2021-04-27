from .node_controller import NodePlainController


class ElementsPlainController(NodePlainController):
    """A Controller specifically for the Bitcoind-process"""

    def __init__(
        self,
        elementsd_path="elements",
        rpcport=18555,
        network="regtest",
        rpcuser="bitcoin",
        rpcpassword="secret",
    ):
        # Just call super and add the node_impl
        super().__init__(
            node_path=elementsd_path,
            rpcport=rpcport,
            network=network,
            rpcuser=rpcuser,
            rpcpassword=rpcpassword,
            node_impl="elements",
        )

    def start_elementsd(
        self,
        cleanup_at_exit=False,
        cleanup_hard=False,
        datadir=None,
        extra_args=[],
        timeout=60,
    ):
        """starts elementsd with a specific rpcport=18543 by default.
        That's not the standard in order to make pytest running while
        developing locally against a different regtest-instance
        """
        # convenience method
        return self.start_node(
            cleanup_at_exit,
            cleanup_hard,
            datadir,
            extra_args,
            timeout,
        )

    def stop_elementsd(self):
        self.stop_node()

    def version(self):
        """ Returns the version of elementsd, e.g. "v0.18.1" """
        version = self.get_rpc().getnetworkinfo()["subversion"]
        version = version.replace("/", "").replace("Elements Core:", "v")
        return version
