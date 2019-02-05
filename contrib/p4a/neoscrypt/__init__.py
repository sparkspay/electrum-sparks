from pythonforandroid.recipe import CythonRecipe


class NeoscryptRecipe(CythonRecipe):
    url = 'git+https://github.com/sparkspay/neoscrypt_module.git'
    version = 'master'

    name = 'neoscrypt'

    depends = [('python3crystax')]

    def get_recipe_env(self, arch):
        '''
        cython has problem with -lpython3.6m , hack to add -L to it
        roughly adapted from similar numpy (fix-numpy branch) dirty solution
        '''

        env = super(NeoscryptRecipe, self).get_recipe_env(arch)
        #: Hack add path L to crystax as a CFLAG

        if 'python3crystax' not in self.ctx.recipe_build_order:
            return env

        api_ver = self.ctx.android_api

        flags = " -L{ctx.ndk_dir}/sources/python/3.6/libs/{arch}/" \
            .format(ctx=self.ctx, arch=arch.arch)
        env['LDFLAGS'] += flags

        return env

recipe = NeoscryptRecipe()
