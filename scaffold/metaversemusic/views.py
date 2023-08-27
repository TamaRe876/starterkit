from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import Playlist, Charts, NFT
from .forms import PlaylistForm, NFTForm, CombinedForm
from web3 import Web3, HTTPProvider
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/e49caa765fe54cc2a3c6c49b241806e2"))


# Create a view to create a new NFT
class CreateNFTView(View):
    template_name = 'metaversemusic/create_nft.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = NFTForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)  # Ensure the user is logged in
    def post(self, request, *args, **kwargs):
        form = CombinedForm(request.POST, request.FILES)
        if form.is_valid():
            nft_instance = form.cleaned_data['nft_form-nft']  # Access the NFTForm field
            genre_instance = form.cleaned_data['genre_form-genre']  # Access the GenreForm field

            # Set the owner as the current user
            nft_instance.owner = request.user

            # Connect to Web3
            web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/e49caa765fe54cc2a3c6c49b241806e2"))
            if web3.isConnected():
                user_profile = request.user.profile  # Get the user's profile
                user_wallet_address = user_profile.bnb_wallet_address

                gas_price = web3.toWei("10", "gwei")  # Gas price in GWei
                gas_limit = 200000  # Gas limit

                # Prepare the transaction
                transaction = {
                    "to": user_wallet_address,  # Recipient address
                    "value": web3.toWei("0.1", "ether"),  # Ether value to send
                    "gas": gas_limit,
                    "gasPrice": gas_price,
                }

                # Sign and send the transaction
                signed_txn = web3.eth.account.signTransaction(transaction, e49caa765fe54cc2a3c6c49b241806e2)
                tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

                # Save the NFT and genre associations
                nft_instance.save()
                nft_instance.genre.add(genre_instance)

                return redirect('nft-detail', nft_id=nft_instance.pk)

        context = {'form': form}
        return render(request, self.template_name, context)

# Create a view to list all the NFTs

def nftsmarket(request):
    nfts = NFT.objects.all()

    return render(request, 'metaversemusic/nftsmarket.html', {'nfts': nfts})


class MintingDetailsView(DetailView):
    template_name = 'metaversemusic/minting_details.html'

    def get(self, request, *args, **kwargs):
        nft_id = kwargs.get('nft_id')
        nft = get_object_or_404(NFT, id=nft_id)
        context = {'nft': nft}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        nft_id = kwargs.get('nft_id')
        nft = get_object_or_404(NFT, id=nft_id)

        minting_cost = request.POST.get('minting_cost')
        royalty_share = request.POST.get('royalty_share')

        nft.minting_cost = minting_cost
        nft.royalty_share = royalty_share
        nft.save()

        # Handle any additional logic or redirects

        context = {'nft': nft, 'success': True}
        return render(request, self.template_name, context)



class PlaylistListView(LoginRequiredMixin, ListView):
    model = Playlist
    template_name = 'metaversemusic/playlist_list.html'
    context_object_name = 'playlists'
    paginate_by = 10


class PlaylistDetailView(LoginRequiredMixin, DetailView):
    model = Playlist
    template_name = 'metaversemusic/playlist_detail.html'
    context_object_name = 'playlist'


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    template_name = 'metaversemusic/playlist_create.html'
    form_class = PlaylistForm

    def form_valid(self, form):
        playlist = form.save(commit=False)
        playlist.user = self.request.user  # Set the user to the current authenticated user
        playlist.save()

        # Process the tags field
        tags_data = form.cleaned_data.get('tags')
        if tags_data:
            # Split the user-provided tags into a list
            tags_list = [tag.strip() for tag in tags_data.split(',') if tag.strip()]
            # Create Tag objects and add them to the playlist's tags
            for tag_name in tags_list:
                tag, created = tags_data.objects.get_or_create(name=tag_name)
                playlist.tags.add(tag)

        return redirect('playlist-list')  # Redirect to the playlist list view


class ChartsListView(ListView):
    model = Charts
    template_name = 'metaversemusic/chart_list.html'
    context_object_name = 'charts'
    paginate_by = 10


class ChartsDetailView(DetailView):
    model = Charts
    template_name = 'metaversemusic/chart_detail.html'
    context_object_name = 'chart'


